#pragma once

#include <JuceHeader.h>
#include <vector>
#include <set>

struct ResonancePeak
{
    float frequency;
    float magnitude;
    float qFactor;

    bool operator<(const ResonancePeak& other) const
    {
        return frequency < other.frequency;
    }

    bool isSimilar(const ResonancePeak& other, float frequencyTolerance = 5.0f) const
    {
        return std::abs(frequency - other.frequency) < frequencyTolerance;
    }
};

class ResonanceDetector
{
public:
    ResonanceDetector();
    ~ResonanceDetector();

    void prepare(double sampleRate, int samplesPerBlock);
    void process(const float* audioData, int numSamples);
    void reset();

    std::vector<ResonancePeak> getDetectedResonances() const;
    void restoreResonances(const std::vector<ResonancePeak>& resonances);
    std::vector<float> getCurrentFFTData() const;

private:
    void detectResonances();
    float calculateQFactor(int binIndex, const std::vector<float>& magnitudes);
    void addResonance(const ResonancePeak& peak);

    static constexpr int FFT_ORDER = 13;
    static constexpr int FFT_SIZE = 1 << FFT_ORDER; // 8192

    juce::dsp::FFT fft;
    juce::dsp::WindowingFunction<float> window;

    std::vector<float> fftData;
    std::vector<float> fifo;
    int fifoIndex;

    std::set<ResonancePeak> detectedResonances;
    std::vector<float> currentSpectrum;

    double sampleRate_;
    float minMagnitudeThreshold;
    float minQFactor;

    juce::CriticalSection resonanceLock;
};
