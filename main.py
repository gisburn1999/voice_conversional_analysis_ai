
from voice_recording import VoiceApp

app = VoiceApp()


def main_menue():
    print("\nLets analyse our togetherness!\n"
          "here are some opportunity's:\n"
          "\n1. Record a sound file and transcribe\n"
          "#2. --- no key --- Analyse the talk (claude)\n"
          "#3. Do a 3 line recap of the talk\n"
          "4. Name the speaker\n"
          "5. GROQ Test\n"
          "q for quit\n"
          "\nAnd some interim solutions for testing purpose:\n"
          "i1. list all names in the conversation\n"
          "6. Load a transcript HARDCODED\n"
          "7. Analyse the speaker with GPT 4 MINI\n"
          "8. Print the actual recording\n"
          "9. Loads the sample Triangle of sadness sound file and transcribes\n"
          )
    while True:
        menue_selection = input("\nEnter your next step: (m for show Menue again) ")
        match menue_selection:
            case "1":
                app.record()
                app.transcribe()
            case "2":
                app.analys_claude()
            case "3":
                pass
            case "4": #name the speaker
                app.name_the_speaker()
            case "5":
                app.analyse_groq()
            case "i1":
                pass
            case "6":
                filepath = "transcripts_prefabricated/before_midnight_generic_version.txt"
                app.open_existing_file(filepath)
            case "7": #Analyse the speaker with GPT 4 MINI
                app.analysis_openAI()
            case "8": # print
                app.print_recording()
            case "9":
                #with open("transcripts/output_20250514_191055.txt" , "r" , encoding="utf-8") as f:


                audio_filepath = "recordings/testfile_talking_with background.m4v"
                #audio_filepath = "recordings/20250524_105941_recording.wav" # long recording with (BELLA)
                #audio_filepath = "recordings/output_20250513_100409.wav"
                print(
                    f"We will load: {audio_filepath}\n"
                    "a hardcoded SOUNDFILE as samplefile\n"
                    )
                txt_filepath = app.transcribe(filepath=audio_filepath)
                print(txt_filepath)

            case "m" | "M":
                main_menue()

            case "q" | "Q":
                print(f"See you the next time")
                exit()


def main():
    main_menue()




if __name__ == "__main__":
    main()