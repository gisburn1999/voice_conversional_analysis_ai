from importlib.metadata import pass_none
#from analyse_with_ai import Ai_Analyse
from voice_recording import VoiceApp
import config
app = VoiceApp()
#aiapp = Ai_Analyse()

def main_menue():
    print("\nLets analyse our togetherness!\n"
          "here are some opportunity's:\n"
          "\n1. Record a sound file and transcribe\n"
          "#2. --- no key --- Analyse the talk (claude)\n"
          "#3. Do a 3 line recap of the talk\n"
          "#4. Great features to come\n"
          "5. GROQ Test\n"
          "q for quit\n"
          "\nAnd some interim solutions for testing purpose:\n"
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
            case "4":
                pass
            case "5":
                app.analyse_groq()
            case "6":
                filepath = "transcripts/output_20250515_175832.txt"
                app.open_existing_file(filepath)
            case "7": #Analyse the speaker with GPT 4 MINI
                app.run_ai_analysis()
            case "8": # print
                app.print_recording()
            case "9":
                #with open("transcripts/output_20250514_191055.txt" , "r" , encoding="utf-8") as f:
                print("We will load:\n"
                      "a hardcoded samplefile as samplefile\n"
                      "enjoy\n")
                audio_filepath = "recordings/triangle_of_sadness_dinner_date_scene.wav"
                #audio_filepath = "triangle_of_sadness_dinner_date_scene.wav"
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