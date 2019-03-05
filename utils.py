from sklearn.preprocessing import MinMaxScaler


######################
# MATH FUNCTIONS #####
######################

# normalize each data
def normalize_min_max(data):
    scaler = MinMaxScaler()
    scaler.fit(data)
    return scaler.transform(data)
