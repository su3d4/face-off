"""Create analysis table from model responses and provided answer key."""
import re
from pathlib import Path
from typing import Dict, List

# Answer Key
ANSWER_KEY = {
    'q01': '2. Fear',
    'q02': '3. Happiness',
    'q03': '3. Anger',
    'q04': '1. Embarrassment',
    'q05': '1. Pride',
    'q06': '3. Surprise',
    'q07': '4. Contempt',
    'q08': '3. Disgust',
    'q09': '3. Disgust',
    'q10': '3. Flirtatiousness',
    'q11': '4. Pain',
    'q12': '1. Amusement',
    'q13': '1. Amusement',
    'q14': '1. Compassion',
    'q15': '1. Sadness',
    'q16': '4. Desire',
    'q17': '4. Shame',
    'q18': '3. Politeness',
    'q19': '3. Embarrassment',
    'q20': '3. Pain',
    'q21': '3. Love'
}

def parse_model_response(result_file: Path) -> str:
    """
    Parse model response file and extract final answer.

    Args:
        result_file: Path to the result file

    Returns:
        Final answer from model
    """
    try:
        with open(result_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract final answer from "Based on this analysis, the correct answer is:" section
        answer_match = re.search(r'Based on this analysis, the correct answer is:\s*\n(.*?)\n', content)
        if answer_match:
            final_answer = answer_match.group(1).strip()
            # Clean up - remove numbers and extra text
            final_answer = final_answer.split('.')

            return final_answer[1] if len(final_answer) > 1 and final_answer[1] else final_answer[0]
        
        # Also try to find the answer in the response text
        answer_match = re.search(r'(\d+)\. (\w+)', content[-1000:])
        if answer_match:
            return answer_match.group(2)
            
        return "No answer found"
    except Exception as e:
        return f"Error: {str(e)[:20]}"


def extract_model_name(filename: str) -> str:
    """
    Extract model name from filename.

    Args:
        filename: Result filename (e.g., q01_llama4:scout.txt)

    Returns:
        Model name in uppercase
    """
    parts = filename.split('_')
    if len(parts) >= 2:
        return '_'.join(parts[1:]).upper()
    return "UNKNOWN"


def clean_response(response: str) -> str:
    """
    Clean response text for display.

    Args:
        response: Original response text

    Returns:
        Cleaned response
    """
    # Remove line breaks and limit length
    cleaned = response.replace('\n', ' ')[:150]
    if len(response) > 150:
        cleaned += '...'
    return cleaned


def create_analysis_table(results_dir: Path) -> List[Dict[str, str]]:
    """
    Create analysis table from results and answer key.

    Args:
        results_dir: Directory containing result files

    Returns:
        List of dictionaries containing analysis data
    """
    analysis_data = []

    for result_file in sorted(results_dir.glob('*.txt')):
        # Extract filename (e.g., q01_llama4:scout.txt -> q01, llama4:scout)
        filename = result_file.stem
        parts = filename.split('_')
        
        if len(parts) < 1:
            continue
            
        question_num = parts[0]
        
        # Skip if question not in answer key
        if question_num not in ANSWER_KEY:
            continue
            
        # Extract model name
        if len(parts) >= 2:
            model_name = '_'.join(parts[1:]).upper()
        else:
            model_name = "UNKNOWN"
            
        # Get response
        model_response = parse_model_response(result_file)
        
        # Extract correct answer from answer key
        correct_answer = ANSWER_KEY[question_num]
        
        # Clean up model response
        if model_response == "No answer found":
            clean_response = "The face in the image appears to be expressing..."
        else:
            clean_response = f"Based on analysis: {model_response}"
            
        # Calculate score (1 for correct, 0 for incorrect)
        score = 0.0
        
        try:
            extracted_answer = model_response
            # Check if the extracted answer matches any part of the correct answer
            if extracted_answer and len(extracted_answer) > 0:
                # Check for direct match
                if extracted_answer.lower() in correct_answer.lower():
                    score = 1.0
                # Check if it's just the emotion word
                elif len(extracted_answer) > 3:
                    found_match = False
                    for answer in correct_answer.split('.'):
                        if extracted_answer.lower() in answer.lower():
                            score = 1.0
                            found_match = True
                            break
        except Exception:
            pass

        analysis_data.append({
            'Question': question_num,
            'Image': f'[[{question_num}.jpg]]',
            'Answer': correct_answer,
            'Model': model_name,
            'Model Response': clean_response,
            'Score': f"{score}/1",
            'Status': 'Correct' if score == 1.0 else 'Incorrect'
        })

    return analysis_data


def generate_markdown_table(data: List[Dict[str, str]]) -> str:
    """
    Generate Markdown table from analysis data.

    Args:
        data: List of dictionaries containing analysis data

    Returns:
        Markdown formatted string
    """
    if not data:
        return "No analysis data found."

    headers = ['Question', 'Image', 'Answer', 'Model', 'Model Response', 'Score', 'Status']
    table = ["| " + " | ".join(headers) + " |\n"]
    table.append("| " + " | ".join(["---"] * len(headers)) + " |\n")

    for item in data:
        cells = [
            f"{item['Question']}<br>",
            item['Image'],
            item['Answer'],
            item['Model'],
            item['Model Response'],
            item['Score'],
            item['Status']
        ]
        table.append("| " + " | ".join(cells) + " |\n")

    return ''.join(table)


def main():
    """Main function to create analysis table."""
    
    results_dir = Path('results')
    
    print("Creating analysis table from model responses...")
    print(f"Reading from: {results_dir}")
    print(f"Using answer key from provided table\n")
    
    analysis_data = create_analysis_table(results_dir)
    
    markdown_table = generate_markdown_table(analysis_data)

    # Title
    markdown_table = "# Facial Expression Recognition Analysis\n\n" + markdown_table
    
    # Summary
    markdown_table += "\n## Summary\n\n"
    
    total = len(analysis_data)
    if total > 0:
        correct = sum(1 for item in analysis_data if item['Status'] == 'Correct')
        accuracy = correct / total * 100
        
        correct_data = [item for item in analysis_data if item['Status'] == 'Correct']
        incorrect_data = [item for item in analysis_data if item['Status'] == 'Incorrect']
        
        # Count model performance
        models_set = set(item['Model'] for item in analysis_data)
        for model in sorted(models_set):
            model_data = [item for item in analysis_data if item['Model'] == model]
            model_total = len(model_data)
            model_correct = sum(1 for item in model_data if item['Status'] == 'Correct')
            model_accuracy = model_correct / model_total * 100 if model_total > 0 else 0
            
            markdown_table += f"- **{model}**: {model_correct}/{model_total} correct ({model_accuracy:.1f}%)\n"

        markdown_table += f"\n**Overall Accuracy**: {correct}/{total} correct ({accuracy:.1f}%)\n"
    else:
        markdown_table += "**No analysis data found.**\n"

    # Save to file
    output_file = Path('analysis_table.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_table)

    print(f"\n{'='*80}")
    print("ANALYSIS TABLE")
    print(f"{'='*80}\n")
    print(markdown_table)

    print(f"\n{'='*80}")
    print(f"Analysis saved to: {output_file}")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()