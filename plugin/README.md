***Plug-in User Manual***


**Specific features of the plug-in logic:**
- Text selection by the user:
- 

- Maximum text length:
  - If the selected text is too long, the plug-in will return 'The selected text extract is too long'
    
- If unrelated risks are detected:
  - Unrelated risks refer to two risk scenarios that are not logically connected to each other
  - The plug-in returns 'Two unrelated risks were detected'
    
- Absolute risk ranges:
  - The tool uses the most conservative value and does calculations based on this value.
    
- Absolute risk < 1%:
  - The tool gives back the absolute risk as 'x / 100.000' to increase comprehensability.
    
- If no risk communication is detected:
  - The tool states that no risk communciation is detected
  - The tool still gives back extracted values and does calculations based on these. 
    
- If verbal descriptors are detected:
  - "nearly doubles, ..." is interpreted as verbal risk descriptor and not as relative risk -> no calculations are made based on this value.
  - "nearly 10%, ..." -> Keine Ahnung, was Tool macht? 

- If the evaluation box only contains a relative risk:
  - a relative risk was detected in the given extract, but no absolute risk could be extracted or calculated.
  - However, the relative risk itself is not enough to make a statement about risks and is therefore intransparent.
- If the evaluation box only contains an absolute risk difference:
  - an absolute risk difference was detected in the given extract, but no absolute risk could be extracted or calculated.
  - However, the absolute risk difference itself is not enough to make a statement about risks and is therefore intransparent.
 


**General information about risk communication**
- Hier links einbauen zu Risikoinformations-Wikis
- Difference between relative risk and relative risk increase/ decrease
