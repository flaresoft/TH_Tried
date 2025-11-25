#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"

class FrequencyMapComponent : public juce::Component, private juce::Timer
{
public:
    FrequencyMapComponent(ResonanceDetectorAudioProcessor& p);
    ~FrequencyMapComponent() override;

    void paint(juce::Graphics& g) override;
    void resized() override;

private:
    void timerCallback() override;
    void drawFrequencyGrid(juce::Graphics& g);
    void drawSpectrum(juce::Graphics& g);
    void drawResonances(juce::Graphics& g);
    float frequencyToX(float frequency) const;
    float magnitudeToY(float magnitude) const;

    ResonanceDetectorAudioProcessor& audioProcessor;
    juce::Rectangle<int> plotArea;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(FrequencyMapComponent)
};

class ResonanceDetectorAudioProcessorEditor : public juce::AudioProcessorEditor
{
public:
    ResonanceDetectorAudioProcessorEditor(ResonanceDetectorAudioProcessor&);
    ~ResonanceDetectorAudioProcessorEditor() override;

    void paint(juce::Graphics&) override;
    void resized() override;

private:
    ResonanceDetectorAudioProcessor& audioProcessor;

    FrequencyMapComponent frequencyMap;
    juce::TextButton resetButton;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(ResonanceDetectorAudioProcessorEditor)
};
