import tkinter as tk
from tkinter import messagebox
import pandas as pd
df = pd.read_csv("/Users/moksh/tweetstest.csv")
df = df.drop("Unnamed: 0", axis = 1)
df['label'] = [0 for row in df.iterrows()]

# Only select tweets without a label
df = df[df["label"] == 0]

# Create the main window
root = tk.Tk()
root.title("Tweet Labeler")

# Create a variable to store the current tweet index
current_index = 0

# Function to display the next tweet
def next_tweet():
    global current_index
    if current_index < df.shape[0]:
        tweet_text.config(state=tk.NORMAL)
        tweet_text.delete("1.0", tk.END)
        tweet_text.insert("1.0", df.iloc[current_index][0])
        tweet_text.config(state=tk.DISABLED)
        current_index += 1
    else:
        messagebox.showinfo("Info", "All tweets have been labeled!")

# Function to assign the label to the current tweet
def assign_label():
    label = label_var.get()
    df.at[current_index-1, "label"] = label
    next_tweet()

# Create a Text widget to display the tweet
tweet_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
tweet_text.pack()

# Create a variable to store the label
label_var = tk.IntVar()

# Create radio buttons for the labels
positive_button = tk.Radiobutton(root, text="Positive", variable=label_var, value=1)
positive_button.pack()
negative_button = tk.Radiobutton(root, text="Negative", variable=label_var, value=-1)
negative_button.pack()
negative_button = tk.Radiobutton(root, text="Neutral", variable=label_var, value=0)
negative_button.pack()

# Create a button to submit the label
submit_button = tk.Button(root, text="Submit", command=assign_label)
submit_button.pack()

# Display the first tweet
next_tweet()

# Run the main loop
root.mainloop()

# Save the labeled dataframe
df.to_csv("labeled_data.csv", index=False)


