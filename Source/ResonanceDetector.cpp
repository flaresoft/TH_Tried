#include "ResonanceDetector.h"

ResonanceDetector::ResonanceDetector()
    : fft(FFT_ORDER)
    , window(FFT_SIZE, juce::dsp::WindowingFunction<float>::hann)
    , fftData(FFT_SIZE * 2, 0.0f)
    , fifo(FFT_SIZE, 0.0f)
    , fifoIndex(0)
    , currentSpectrum(FFT_SIZE / 2, 0.0f)
    , sampleRate_(44100.0)
    , minMagnitudeThreshold(0.01f)  // -40 dB
    , minQFactor(2.0f)               // Minimum Q factor for resonance
{
}

ResonanceDetector::~ResonanceDetector()
{
}

void ResonanceDetector::prepare(double sampleRate, int samplesPerBlock)
{
    juce::ignoreUnused(samplesPerBlock);
    sampleRate_ = sampleRate;
}

void ResonanceDetector::process(const float* audioData, int numSamples)
{
    // Fill FIFO buffer
    for (int i = 0; i < numSamples; ++i)
    {
        fifo[fifoIndex] = audioData[i];
        fifoIndex++;

        // When FIFO is full, perform FFT
        if (fifoIndex >= FFT_SIZE)
        {
            fifoIndex = 0;

            // Copy FIFO to FFT data
            std::copy(fifo.begin(), fifo.end(), fftData.begin());

            // Apply window
            window.multiplyWithWindowingTable(fftData.data(), FFT_SIZE);

            // Perform FFT
            fft.performFrequencyOnlyForwardTransform(fftData.data());

            // Store current spectrum for visualization
            for (int j = 0; j < FFT_SIZE / 2; ++j)
            {
                currentSpectrum[j] = fftData[j];
            }

            // Detect resonances
            detectResonances();
        }
    }
}

void ResonanceDetector::detectResonances()
{
    std::vector<float> magnitudes(FFT_SIZE / 2);

    // Convert to dB and normalize
    float maxMagnitude = 0.0f;
    for (int i = 0; i < FFT_SIZE / 2; ++i)
    {
        magnitudes[i] = fftData[i];
        maxMagnitude = std::max(maxMagnitude, magnitudes[i]);
    }

    if (maxMagnitude < 1e-6f)
        return;

    // Normalize
    for (auto& mag : magnitudes)
    {
        mag /= maxMagnitude;
    }

    // Find peaks using simple peak detection
    // A peak is a local maximum that exceeds threshold and has sufficient Q
    for (int i = 10; i < FFT_SIZE / 2 - 10; ++i) // Skip DC and very low/high frequencies
    {
        float currentMag = magnitudes[i];

        // Check if it's a local maximum
        bool isPeak = true;
        for (int j = -5; j <= 5; ++j)
        {
            if (j != 0 && magnitudes[i + j] > currentMag)
            {
                isPeak = false;
                break;
            }
        }

        if (isPeak && currentMag > minMagnitudeThreshold)
        {
            // Calculate Q factor
            float q = calculateQFactor(i, magnitudes);

            if (q >= minQFactor)
            {
                // Calculate frequency
                float frequency = (i * static_cast<float>(sampleRate_)) / FFT_SIZE;

                ResonancePeak peak;
                peak.frequency = frequency;
                peak.magnitude = currentMag;
                peak.qFactor = q;

                addResonance(peak);
            }
        }
    }
}

float ResonanceDetector::calculateQFactor(int binIndex, const std::vector<float>& magnitudes)
{
    float peakMag = magnitudes[binIndex];
    float halfPowerLevel = peakMag / std::sqrt(2.0f);

    // Find -3dB points (half power)
    int lowerBin = binIndex;
    int upperBin = binIndex;

    // Find lower -3dB point
    for (int i = binIndex - 1; i >= 1; --i)
    {
        if (magnitudes[i] <= halfPowerLevel)
        {
            lowerBin = i;
            break;
        }
    }

    // Find upper -3dB point
    for (int i = binIndex + 1; i < static_cast<int>(magnitudes.size()) - 1; ++i)
    {
        if (magnitudes[i] <= halfPowerLevel)
        {
            upperBin = i;
            break;
        }
    }

    // Calculate Q factor: Q = f0 / (f2 - f1)
    float centerFreq = (binIndex * static_cast<float>(sampleRate_)) / FFT_SIZE;
    float lowerFreq = (lowerBin * static_cast<float>(sampleRate_)) / FFT_SIZE;
    float upperFreq = (upperBin * static_cast<float>(sampleRate_)) / FFT_SIZE;

    float bandwidth = upperFreq - lowerFreq;

    if (bandwidth < 1.0f)
        bandwidth = 1.0f;

    return centerFreq / bandwidth;
}

void ResonanceDetector::addResonance(const ResonancePeak& peak)
{
    juce::ScopedLock lock(resonanceLock);

    // Check if similar resonance already exists
    bool found = false;
    for (auto& existing : detectedResonances)
    {
        if (existing.isSimilar(peak, 10.0f))
        {
            // Update if new peak has higher magnitude
            if (peak.magnitude > existing.magnitude)
            {
                detectedResonances.erase(existing);
                detectedResonances.insert(peak);
            }
            found = true;
            break;
        }
    }

    if (!found)
    {
        detectedResonances.insert(peak);
    }
}

void ResonanceDetector::reset()
{
    juce::ScopedLock lock(resonanceLock);
    detectedResonances.clear();
}

std::vector<ResonancePeak> ResonanceDetector::getDetectedResonances() const
{
    juce::ScopedLock lock(resonanceLock);
    return std::vector<ResonancePeak>(detectedResonances.begin(), detectedResonances.end());
}

void ResonanceDetector::restoreResonances(const std::vector<ResonancePeak>& resonances)
{
    juce::ScopedLock lock(resonanceLock);
    detectedResonances.clear();
    detectedResonances.insert(resonances.begin(), resonances.end());
}

std::vector<float> ResonanceDetector::getCurrentFFTData() const
{
    return currentSpectrum;
}
