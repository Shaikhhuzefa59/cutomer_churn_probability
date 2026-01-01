import pandas as pd

def preprocess(filepath, scaler):
    df = pd.read_csv(filepath)

    # Contract length mapping
    li = []
    for val in df['Contract Length']:
        if val=='Monthly':
            li.append(1)
        elif val=='Quarterly':
            li.append(3)
        else:
            li.append(12)
    df['Contract_month'] = li
    # Avg monthly spend
    df['Avg_monthly_spend'] = round(df['Total Spend'] / df['Contract_month'], 2)

    # drop customerID, Contract Length
    df.drop(['CustomerID', 'Contract Length'], axis=1, inplace=True)

    # Tenure bucket
    df['Tenure Bucket'] = pd.cut(
        df['Tenure'],
        bins=[-1,6,12,float('inf')],
        labels=['Short','Medium', 'Long']
    )
    # Encoding
    df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1})
    df['Subscription Type'] = df['Subscription Type'].map(
        {'Basic': 0, 'Standard': 1, 'Premium': 2}
    )
    df['Tenure Bucket'] = df['Tenure Bucket'].map({'Short':0, 'Medium':1, 'Long':2})
    df['Tenure Bucket'].astype(int)


    # Scaling
    cols = ['Age', 'Tenure', 'Usage Frequency','Support Calls','Payment Delay','Avg_monthly_spend','Total Spend','Contract_month','Last Interaction']
    df[cols] = scaler.transform(df[cols])

    return df



