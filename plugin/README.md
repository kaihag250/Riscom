***Plug-in User Manual***


**Specific features of the plug-in logic:**
- **User-driven text selection:**
  - The user must select a relevant text section manually
  - The tool only analyzes the selected passage after clicking "Analyze"
  - Risk communication can only be detected within the selected text

- **Maximum text length:**
  - If the selected text is too long, the plug-in returns: *'The selected text extract is too long'*
    
- **Unrelated risks:**
  - *Unrelated risks* refer to two risk scenarios that are not logically connected to each other
  - The plug-in returns: *'Two unrelated risks were detected'*
    
- **Risk ranges:**
  - If a risk is stated as a range (e.g. between 10% and 15%), the tool uses the midpoint value for further calculations
  - **Please note:** The midpoint is a simpfliciation and does **not capture the uncertainty** of the original range.
                 Users should avoid relying solely on this value in sensitive interpretations.
    
- **Absolute risk < 1%:**
  - Risks below 1% are displayed as *x / 100,000* to improve clarity and readability.
    
- **No risk communication detected:**
  - The tool reports that no risk communciation was found.
  - The tool immediately stops and does not continue with extracting values. 
    
- **Verbal descriptors are detected:**
  - If the text contains an approximate statement like "The absolute risk is nearly 10%",
    the tool interprets this as a quantitative value and treats it as 10% in further calculations.
  - However, if the text contains a relative formulation like "The risk almost doubles",
    the tool recognizes this as a verbal descriptor and does not assign a numerical value.
  - Reason: Absolute approximations still provide a usable number, while relative phrases lack a clear reference point and are too
            ambiguous to quantify reliably.
    

- **Only a relative risk is detected:**
  - - A relative risk is identified, but no absolute risk could be extracted or calculated.
  - ⚠️ A relative risk alone is **not sufficient to interpret risk levels**

- **Only an absolute risk difference is detected:**
  - An absolute risk difference is identified, but no absolute risks could be extracted or calculated.
  - ⚠️ An absolute risk difference alone is also **insufficient for meaningful interpretation**
 


**General information about risk communication**
- Hier links einbauen zu Risikoinformations-Wikis
- Difference between relative risk and relative risk increase/ decrease
