import pandas as pd

# load excel
df = pd.read_excel("inference_testing_results.xlsx")

# csv file
df.to_csv("model_output.csv", index=False)

print("data as csv")
