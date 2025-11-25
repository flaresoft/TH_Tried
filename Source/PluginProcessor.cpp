#include "PluginProcessor.h"
#include "PluginEditor.h"

ResonanceDetectorAudioProcessor::ResonanceDetectorAudioProcessor()
    : AudioProcessor(BusesProperties()
                     .withInput("Input", juce::AudioChannelSet::stereo(), true)
                     .withOutput("Output", juce::AudioChannelSet::stereo(), true))
{
}

ResonanceDetectorAudioProcessor::~ResonanceDetectorAudioProcessor()
{
}

const juce::String ResonanceDetectorAudioProcessor::getName() const
{
    return JucePlugin_Name;
}

bool ResonanceDetectorAudioProcessor::acceptsMidi() const
{
    return false;
}

bool ResonanceDetectorAudioProcessor::producesMidi() const
{
    return false;
}

bool ResonanceDetectorAudioProcessor::isMidiEffect() const
{
    return false;
}

double ResonanceDetectorAudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int ResonanceDetectorAudioProcessor::getNumPrograms()
{
    return 1;
}

int ResonanceDetectorAudioProcessor::getCurrentProgram()
{
    return 0;
}

void ResonanceDetectorAudioProcessor::setCurrentProgram(int index)
{
    juce::ignoreUnused(index);
}

const juce::String ResonanceDetectorAudioProcessor::getProgramName(int index)
{
    juce::ignoreUnused(index);
    return {};
}

void ResonanceDetectorAudioProcessor::changeProgramName(int index, const juce::String& newName)
{
    juce::ignoreUnused(index, newName);
}

void ResonanceDetectorAudioProcessor::prepareToPlay(double sampleRate, int samplesPerBlock)
{
    resonanceDetector.prepare(sampleRate, samplesPerBlock);
}

void ResonanceDetectorAudioProcessor::releaseResources()
{
}

bool ResonanceDetectorAudioProcessor::isBusesLayoutSupported(const BusesLayout& layouts) const
{
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
     && layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

    if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
        return false;

    return true;
}

void ResonanceDetectorAudioProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ignoreUnused(midiMessages);
    juce::ScopedNoDenormals noDenormals;

    auto totalNumInputChannels = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();

    // Clear unused output channels
    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear(i, 0, buffer.getNumSamples());

    // Process audio for resonance detection (mix to mono if stereo)
    if (totalNumInputChannels > 0)
    {
        const int numSamples = buffer.getNumSamples();
        std::vector<float> monoBuffer(numSamples);

        // Mix to mono
        for (int channel = 0; channel < totalNumInputChannels; ++channel)
        {
            const float* channelData = buffer.getReadPointer(channel);
            for (int i = 0; i < numSamples; ++i)
            {
                monoBuffer[i] += channelData[i] / totalNumInputChannels;
            }
        }

        // Process through resonance detector
        resonanceDetector.process(monoBuffer.data(), numSamples);
    }
}

bool ResonanceDetectorAudioProcessor::hasEditor() const
{
    return true;
}

juce::AudioProcessorEditor* ResonanceDetectorAudioProcessor::createEditor()
{
    return new ResonanceDetectorAudioProcessorEditor(*this);
}

void ResonanceDetectorAudioProcessor::getStateInformation(juce::MemoryBlock& destData)
{
    // Save detected resonances
    auto resonances = resonanceDetector.getDetectedResonances();
    juce::MemoryOutputStream stream(destData, false);

    stream.writeInt(static_cast<int>(resonances.size()));
    for (const auto& peak : resonances)
    {
        stream.writeFloat(peak.frequency);
        stream.writeFloat(peak.magnitude);
        stream.writeFloat(peak.qFactor);
    }
}

void ResonanceDetectorAudioProcessor::setStateInformation(const void* data, int sizeInBytes)
{
    // Restore detected resonances
    juce::MemoryInputStream stream(data, static_cast<size_t>(sizeInBytes), false);

    int numResonances = stream.readInt();
    std::vector<ResonancePeak> resonances;

    for (int i = 0; i < numResonances; ++i)
    {
        ResonancePeak peak;
        peak.frequency = stream.readFloat();
        peak.magnitude = stream.readFloat();
        peak.qFactor = stream.readFloat();
        resonances.push_back(peak);
    }

    resonanceDetector.restoreResonances(resonances);
}

std::vector<ResonancePeak> ResonanceDetectorAudioProcessor::getDetectedResonances() const
{
    return resonanceDetector.getDetectedResonances();
}

void ResonanceDetectorAudioProcessor::resetResonances()
{
    resonanceDetector.reset();
}

std::vector<float> ResonanceDetectorAudioProcessor::getCurrentFFTData() const
{
    return resonanceDetector.getCurrentFFTData();
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new ResonanceDetectorAudioProcessor();
}
