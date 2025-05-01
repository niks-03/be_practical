from collections import defaultdict
from multiprocessing import Pool

class GradeCalculator:
    def __init__(self, input_file):
        self.input_file = input_file
        
    def mapper(self, line):
        """Map function: processes each line and returns (name, score) pairs"""
        try:
            name, score = line.strip().split(',')
            score = int(score)
            return (name, score)
        except ValueError:
            print(f"Warning: Skipping invalid line '{line.strip()}'")
            return None
            
    def reducer(self, name_scores):
        """Reduce function: calculates average and grade for each student"""
        name, scores = name_scores
        if not scores:
            return None
            
        average_score = sum(scores) / len(scores)
        
        # Determine the grade based on the average score
        if average_score >= 90:
            grade = 'A'
        elif average_score >= 80:
            grade = 'B'
        elif average_score >= 70:
            grade = 'C'
        elif average_score >= 60:
            grade = 'D'
        else:
            grade = 'F'
            
        return {
            'name': name,
            'average': round(average_score, 2),
            'grade': grade,
            'scores': scores
        }

def main():
    print("Student Grade Calculator (MapReduce Implementation)")
    print("------------------------------------------------")
    
    # Get input file
    input_file = input("Enter the path to the scores file: ").strip()
    if not input_file:
        print("Error: File path cannot be empty.")
        return
        
    try:
        # Read input file
        with open(input_file, 'r') as file:
            lines = file.readlines()
            
        # Create calculator instance
        calculator = GradeCalculator(input_file)
        
        # Map phase: Process each line in parallel
        with Pool() as pool:
            mapped_results = pool.map(calculator.mapper, lines)
            mapped_results = [r for r in mapped_results if r is not None]
            
        # Group by name (shuffle phase)
        grouped_data = defaultdict(list)
        for name, score in mapped_results:
            grouped_data[name].append(score)
            
        # Reduce phase: Calculate final results
        with Pool() as pool:
            reduced_results = pool.map(calculator.reducer, grouped_data.items())
            reduced_results = [r for r in reduced_results if r is not None]
            
        # Display results
        if not reduced_results:
            print("No valid scores were processed.")
            return
            
        print("\nResults:")
        print("--------")
        for result in sorted(reduced_results, key=lambda x: x['name']):
            print(f"\nStudent: {result['name']}")
            print(f"Scores: {result['scores']}")
            print(f"Average: {result['average']}")
            print(f"Grade: {result['grade']}")
            
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()