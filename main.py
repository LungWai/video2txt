
import convert

def main():
    # Input file location
    input_file = "input/input.mp4"
    
    # Output file location
    output_file = "output/output.docx"
    
    # Choose output format
    output_format = "docx"  # or "text"
    
    # Convert mp4 video to docx or text file
    convert.convert_video_to_text(input_file, output_file, output_format)

if __name__ == "__main__":
    main()

