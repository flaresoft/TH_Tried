#include "PluginProcessor.h"
#include "PluginEditor.h"

// FrequencyMapComponent implementation
FrequencyMapComponent::FrequencyMapComponent(ResonanceDetectorAudioProcessor& p)
    : audioProcessor(p)
{
    startTimerHz(30); // 30 FPS refresh rate
}

FrequencyMapComponent::~FrequencyMapComponent()
{
    stopTimer();
}

void FrequencyMapComponent::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colour(0xff1a1a1a));

    plotArea = getLocalBounds().reduced(40, 20);

    drawFrequencyGrid(g);
    drawSpectrum(g);
    drawResonances(g);
}

void FrequencyMapComponent::resized()
{
}

void FrequencyMapComponent::timerCallback()
{
    repaint();
}

void FrequencyMapComponent::drawFrequencyGrid(juce::Graphics& g)
{
    g.setColour(juce::Colour(0xff404040));

    // Draw frequency grid lines
    const float frequencies[] = { 20.0f, 50.0f, 100.0f, 200.0f, 500.0f, 1000.0f,
                                  2000.0f, 5000.0f, 10000.0f, 20000.0f };

    for (float freq : frequencies)
    {
        float x = frequencyToX(freq);
        g.drawLine(x, plotArea.getY(), x, plotArea.getBottom(), 1.0f);

        // Draw frequency labels
        g.setColour(juce::Colour(0xff808080));
        juce::String label;
        if (freq >= 1000.0f)
            label = juce::String(freq / 1000.0f, 1) + "k";
        else
            label = juce::String(static_cast<int>(freq));

        g.drawText(label, static_cast<int>(x) - 20, plotArea.getBottom() + 5, 40, 15,
                   juce::Justification::centred);
        g.setColour(juce::Colour(0xff404040));
    }

    // Draw magnitude grid lines
    for (int db = -60; db <= 0; db += 10)
    {
        float magnitude = juce::Decibels::decibelsToGain(static_cast<float>(db));
        float y = magnitudeToY(magnitude);
        g.drawLine(plotArea.getX(), y, plotArea.getRight(), y, 1.0f);

        // Draw dB labels
        g.setColour(juce::Colour(0xff808080));
        g.drawText(juce::String(db) + " dB", plotArea.getX() - 35, static_cast<int>(y) - 7,
                   30, 14, juce::Justification::right);
        g.setColour(juce::Colour(0xff404040));
    }
}

void FrequencyMapComponent::drawSpectrum(juce::Graphics& g)
{
    auto fftData = audioProcessor.getCurrentFFTData();
    if (fftData.empty())
        return;

    juce::Path spectrumPath;
    bool started = false;

    const int numBins = static_cast<int>(fftData.size());
    const double sampleRate = audioProcessor.getSampleRate();

    for (int i = 1; i < numBins; ++i)
    {
        float frequency = (i * static_cast<float>(sampleRate)) / (numBins * 2);

        if (frequency < 20.0f || frequency > 20000.0f)
            continue;

        float x = frequencyToX(frequency);
        float y = magnitudeToY(fftData[i]);

        if (!started)
        {
            spectrumPath.startNewSubPath(x, y);
            started = true;
        }
        else
        {
            spectrumPath.lineTo(x, y);
        }
    }

    g.setColour(juce::Colour(0xff00aaff).withAlpha(0.6f));
    g.strokePath(spectrumPath, juce::PathStrokeType(1.5f));
}

void FrequencyMapComponent::drawResonances(juce::Graphics& g)
{
    auto resonances = audioProcessor.getDetectedResonances();

    for (const auto& peak : resonances)
    {
        if (peak.frequency < 20.0f || peak.frequency > 20000.0f)
            continue;

        float x = frequencyToX(peak.frequency);
        float y = magnitudeToY(peak.magnitude);

        // Draw resonance marker
        g.setColour(juce::Colours::red);
        g.fillEllipse(x - 4, y - 4, 8, 8);

        // Draw vertical line
        g.setColour(juce::Colours::red.withAlpha(0.5f));
        g.drawLine(x, plotArea.getY(), x, plotArea.getBottom(), 1.0f);

        // Draw frequency label
        g.setColour(juce::Colours::white);
        juce::String freqLabel;
        if (peak.frequency >= 1000.0f)
            freqLabel = juce::String(peak.frequency / 1000.0f, 2) + " kHz";
        else
            freqLabel = juce::String(static_cast<int>(peak.frequency)) + " Hz";

        freqLabel += "\nQ: " + juce::String(peak.qFactor, 1);

        g.drawText(freqLabel, static_cast<int>(x) - 40, static_cast<int>(y) - 35,
                   80, 30, juce::Justification::centred);
    }
}

float FrequencyMapComponent::frequencyToX(float frequency) const
{
    // Logarithmic frequency scale (20 Hz to 20 kHz)
    const float minFreq = 20.0f;
    const float maxFreq = 20000.0f;

    float normalized = (std::log10(frequency) - std::log10(minFreq)) /
                       (std::log10(maxFreq) - std::log10(minFreq));

    return plotArea.getX() + normalized * plotArea.getWidth();
}

float FrequencyMapComponent::magnitudeToY(float magnitude) const
{
    // Convert to dB and map to Y position
    float db = juce::Decibels::gainToDecibels(magnitude, -60.0f);
    float normalized = juce::jmap(db, -60.0f, 0.0f, 1.0f, 0.0f);

    return plotArea.getY() + normalized * plotArea.getHeight();
}

// ResonanceDetectorAudioProcessorEditor implementation
ResonanceDetectorAudioProcessorEditor::ResonanceDetectorAudioProcessorEditor(ResonanceDetectorAudioProcessor& p)
    : AudioProcessorEditor(&p)
    , audioProcessor(p)
    , frequencyMap(p)
{
    addAndMakeVisible(frequencyMap);
    addAndMakeVisible(resetButton);

    resetButton.setButtonText("Reset Resonances");
    resetButton.onClick = [this]
    {
        audioProcessor.resetResonances();
    };

    setSize(800, 500);
}

ResonanceDetectorAudioProcessorEditor::~ResonanceDetectorAudioProcessorEditor()
{
}

void ResonanceDetectorAudioProcessorEditor::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colour(0xff2a2a2a));

    g.setColour(juce::Colours::white);
    g.setFont(20.0f);
    g.drawText("Resonance Detector", getLocalBounds().removeFromTop(40),
               juce::Justification::centred);
}

void ResonanceDetectorAudioProcessorEditor::resized()
{
    auto bounds = getLocalBounds();

    // Title area
    bounds.removeFromTop(40);

    // Reset button at bottom
    auto buttonArea = bounds.removeFromBottom(50);
    resetButton.setBounds(buttonArea.reduced(20, 10));

    // Frequency map in the middle
    frequencyMap.setBounds(bounds);
}
