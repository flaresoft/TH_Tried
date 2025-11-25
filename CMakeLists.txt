cmake_minimum_required(VERSION 3.15)

project(ResonanceDetector VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add JUCE as a subdirectory (you'll need to clone JUCE or add it as a submodule)
# For now, we'll use FetchContent to download JUCE
include(FetchContent)

FetchContent_Declare(
    JUCE
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 7.0.9
)

FetchContent_MakeAvailable(JUCE)

# Create the VST3 plugin
juce_add_plugin(ResonanceDetector
    COMPANY_NAME "FlareStudio"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE
    PLUGIN_MANUFACTURER_CODE Flre
    PLUGIN_CODE Rsdt
    FORMATS VST3
    PRODUCT_NAME "Resonance Detector"
)

# Add source files
target_sources(ResonanceDetector
    PRIVATE
        Source/PluginProcessor.cpp
        Source/PluginEditor.cpp
        Source/ResonanceDetector.cpp
)

# Add header files
target_include_directories(ResonanceDetector
    PUBLIC
        Source
)

# Link JUCE modules
target_compile_definitions(ResonanceDetector
    PUBLIC
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
        JUCE_VST3_CAN_REPLACE_VST2=0
)

target_link_libraries(ResonanceDetector
    PRIVATE
        juce::juce_audio_utils
        juce::juce_dsp
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags
)
