def detect_sleep_stage(hrv, rolling_mean, rolling_std):
    """
    Detect sleep stage based on HRV and other features.

    Parameters:
    hrv (float): Heart rate variability.
    rolling_mean (float): Rolling mean of heart rate.
    rolling_std (float): Rolling standard deviation of heart rate.

    Returns:
    str: Detected sleep stage ('wake', 'rem', 'light_sleep', 'deep_sleep').
    """
    if rolling_mean > 0.8:  # Example threshold, adjust based on your data
        return 'wake'
    elif rolling_std < 0.5 and hrv > 1.0:
        return 'rem'
    elif rolling_std < 0.5:
        return 'deep_sleep'
    else:
        return 'light_sleep'
