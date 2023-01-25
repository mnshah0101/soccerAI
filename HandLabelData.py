import tkinter as tk
from tkinter import messagebox
import pandas as pd
import copy
df_og = pd.read_csv("labeled_data.csv", )
df_og = df_og[['text', 'date', 'label']]

DF = copy.deepcopy(df_og)
starting_index = len(DF)
for i in range(len(DF)):
    if DF['label'][i]==2:
        starting_index = i
        break

# Only select tweets without a label
df = DF.iloc[starting_index:]
input_labels = []

# Create the main window
root = tk.Tk()
root.title("Tweet Labeler")

# Create a variable to store the current tweet index
current_index = 0

# Function to display the next tweet
def next_tweet(root):
    global current_index
    if current_index < df.shape[0]:
        tweet_text.config(state=tk.NORMAL)
        tweet_text.delete("1.0", tk.END)
        tweet_text.insert("1.0", df.iloc[current_index]['text'])
        tweet_text.config(state=tk.DISABLED)
        current_index += 1
    else:
        messagebox.showinfo("Info", "All tweets have been labeled!")

# Function to assign the label to the current tweet
def assign_label():
    global root
    label = label_var.get()
    input_labels.append(label)
    next_tweet(root)

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
exit_button = tk.Button(root, text="Done", command=root.destroy)
exit_button.pack(pady=20)


# Display the first tweet
next_tweet(root)

# Run the main loop
root.mainloop()

# Save the labeled dataframe

current_index = current_index
full_labels = list(DF['label'])

old_labels = list(DF['label'][:starting_index])
new_labels = input_labels
first_labels = old_labels+new_labels
last_labels = [2 for i in range(len(full_labels)-len(first_labels))]
labels = first_labels+last_labels
DF['label'] = labels
DF.to_csv("labeled_data.csv", index = False)
