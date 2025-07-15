from ollama import chat

# 1 Prompt für die Analyse vorbereiten
if risk_comm := input("Enter the sentence containing risk communication: "):
    prompt = f"""
You are a risk communication analysis assistant.

Your task is to analyze the following text and extract structured risk communication data.

First, determine if the text contains risk communication. If it does, set "Risk communication: 1". Otherwise, set it to "Risk communication: 0" and return null for all other fields.

Return the result as plain text using the format:  
Field name: value  
Use one field per line, and write "null" if the value is not available.

Here are the fields you should extract, along with a short explanation:

- risk_communication: 1 if the sentence communicates risk; otherwise 0  
- absolute_risk_base_case): % or ratio before any intervention (e.g. "10%" or "30 in 1000")  
- absolute_risk_new: % or ratio after intervention or change  
- absolute_number_base: count of affected individuals before change  
- absolute_number_new: count of affected individuals after change  
- absolute_risk_difference: difference between base and new risk (e.g. "5%")  
- relative_risk: relative change (e.g. "10% increase", "50% reduction")  
- absolute_number_difference: change in absolute numbers (e.g. "500 fewer")  
- verbal_risk_descriptor_base: qualitative risk term before change (e.g. "rare")  
- verbal_risk_descriptor_new: qualitative term after change (e.g. "high risk")  
- verbal_risk_descriptor_change: e.g. "significantly higher"  
- population_size: higher-level population the risk applies to  
- reference_class_size_base: total population size for base case  
- reference_class_size_new: total population size for new case  
- reference_class_description_base: group description (e.g. "general population")  
- reference_class_description_new: changed group (e.g. "patients on aspirin")  
- source_base: where the base risk data comes from (e.g. "CDC")  
- source_new: source for the changed/new risk (e.g. "NHS")  
- topic_and_unit: what the risk is about, and the time or unit it refers to (e.g. "lung cancer per year")

---

Example:

Text:  
"The risk of heart failure is 10%. By taking our medication, it decreases to 5%. This result comes from a study on 100,000 patients from the general population."

Output:  
Risk communication: 1  
Absolute risk (base case): 10%  
Absolute risk (new case): 5%  
Absolute number (base case): null  
Absolute number (new case): null  
Absolute risk difference: 5%  
Relative risk: 50%  
Absolute number difference: null  
Verbal risk descriptor (base case): null  
Verbal risk descriptor (new situation): null  
Verbal risk descriptor (change from base to new): null  
Reference class size (base case: absolute number): 100000  
Reference class size (new case: absolute number): 100000  
Reference class description (base case): general population  
Reference class description (new case): general population  
Population (übergeordnete Grundgesamtheit): null  
Source (base case): null  
Source (new situation): null  
Topic and unit: heart failure risk per person

Now analyze the following text:  


"{risk_comm}"

"""


# 2 Request an das LLM senden
    response = chat(
        model="mistral:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={"temperature": 0.7},  # ausprobieren, wie sich Ergebnisse verhalten
    )

    print(response)

# example1: The risk of heart failure is 10%. By taking our medication, it decreases to 5%. 
# example2: The risk of heart failure is 10 in 200 people. By taking our medication, it is 50% smaller.
