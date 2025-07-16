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
  - If a risk is stated as a range (e.g. between 10% and 15%), the tool often has difficulties handling these.
  - Please carefully double check the tool output!
    
- **Absolute risk < 1%:**
  - Risks below 1% are also displayed as *x / 100,000* to improve clarity and readability.
    
- **Dealing with verbal risk descriptors:**
  - The tool handles verbal risk descriptors connected to quantitative information differently:
  - If the text contains an approximate statement like "The absolute risk is nearly 10%",
    the tool interprets this as a quantitative value and treats it as 10% in further calculations.
  - ⚠️ However, if the text contains a relative formulation like "The risk almost doubles",
    the tool recognizes this as a verbal descriptor and does not assign a numerical value.
    
- **No risk communication detected:**
  - The tool reports that no risk communciation was found.
  - The tool immediately stops and does not continue with extracting values. 
    
- **Only a relative risk is detected:**
  - A relative risk is identified, but no absolute risk could be extracted or calculated.
  - ⚠️ A relative risk alone is **not sufficient to interpret risk levels**

- **Only an absolute risk difference is detected:**
  - An absolute risk difference is identified, but no absolute risks could be extracted or calculated.
  - ⚠️ An absolute risk difference alone is also **insufficient for meaningful interpretation**
 


**General information about risk communication**
- **What is a risk?**
  - A risk describes how likely it is that a specific event will occur. The term refers to probability and is not limited to negative
    outcomes, although it often is in everyday understanding. In the context of risk communication, the term "risk" can typically be
    replaced by "likelihood".
  
- **When is risk communication transparent?**
  - If the text describes only one risk scenario, the communication is transparent only if the absolute risk is stated.
  - If the text describes two risk scenarios (referred to as base case and new case), the communication is transparent only if the
    absolute risk is reported for both cases.

- **Verbal descriptors are detected:**
  - ⚠️ Be careful when trying to interpret verbal risk descriptors, e.g. high risk, since they can mean many different things if not
       explicitly defined.
    
- **Definitions of important terms for understanding risk communication:**
  - **Absolute risk:**
    
    Absolute risk refers to the actual probability that a specific event (e.g., illness, recovery, death) occurs in a group.
    It is preferred over relative risk and should always be reported for all comparison groups or time points.
    It can be expressed as percentages or as natural frequencies (e.g., “5 out of 100 people”).
  - **Absolute risk difference:**
    
    Absolute risk difference is the numerical difference between two absolute risks (e.g., 0.06% – 0.02% = 0.04 percentage points).
    It reflects the actual change in risk.
    Unlike relative risk, it avoids overestimating effects when the base risk is low.
    A large relative risk can still correspond to a small absolute risk difference.
  - **Relative risk:**
    
    A relative risk compares the likelihood of an event between two groups — often expressed as multiples ("3 times more likely").
    The relative risk is the ratio between two risks.
    In our tool, the relative risk is defined as follows:
    relative risk = absolute risk in the new case / absolute risk in the base case
    Attention: Relative risks can easily be misleading and tend to cause overestimation of actual risk.
    They should never be presented without the corresponding absolute risks (especially the baseline risk in the comparison group).
    Transparent communication requires at least stating at the absolute risk for the base case.
  - **Relative risk increase/ decrease:**
    
    Describes how much the risk increases or decreases in relative terms between two groups. The change is expressed as percentage above
    or below the base.
    It is calculated as follows:
    Relative Risk Increase = (Relative risk − 1) × 100% (if Relative risk > 1)
    Relative Risk Decrease = (1 − Relative risk) × 100% (if Relative risk < 1)
    Example: A relative risk of 0.5 means a 50% risk reduction.
  - **Reference class:**
    
    Specifies the group of people or cases to which the risk statement applies.
    It defines the denominator or population context, such as:
    “Smokers aged 50–70”, “Women with pre-existing conditions”, or “Children under 5”.
    Clear reference classes are essential for correct interpretation of any risk.
