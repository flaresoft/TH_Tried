#pragma once

#include <JuceHeader.h>
#include "ResonanceDetector.h"

class ResonanceDetectorAudioProcessor : public juce::AudioProcessor
{
public:
    ResonanceDetectorAudioProcessor();
    ~ResonanceDetectorAudioProcessor() override;

    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

    bool isBusesLayoutSupported(const BusesLayout& layouts) const override;

    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram(int index) override;
    const juce::String getProgramName(int index) override;
    void changeProgramName(int index, const juce::String& newName) override;

    void getStateInformation(juce::MemoryBlock& destData) override;
    void setStateInformation(const void* data, int sizeInBytes) override;

    // Get detected resonances
    std::vector<ResonancePeak> getDetectedResonances() const;

    // Reset detected resonances
    void resetResonances();

    // Get current FFT data for visualization
    std::vector<float> getCurrentFFTData() const;

private:
    ResonanceDetector resonanceDetector;
    juce::AudioBuffer<float> bufferCopy;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(ResonanceDetectorAudioProcessor)
};
