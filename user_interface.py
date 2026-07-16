import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Regex Tool")

    search_validate_var = tk.BooleanVar()
    search_replace_var = tk.BooleanVar()

    def highlight_selection():
        focused = root.focus_get()
        if not isinstance(focused, tk.Text):
            return
        try:
            start = focused.index(tk.SEL_FIRST)
            end = focused.index(tk.SEL_LAST)
            text = focused.get(start, end)
            focused.delete(start, end)
            focused.insert(start, text)
            focused.tag_add("highlight", start, f"{start}+{len(text)}c")
        except tk.TclError:
            pass  # no text selected

    def on_submit():
        before = text_before.get("1.0", tk.END).strip()
        after = text_after.get("1.0", tk.END).strip()
        print("Before:\n", before)
        print("\nAfter:\n", after)

    tk.Checkbutton(root, text="Search/Validate",
                   variable=search_validate_var).pack(pady=5)
    tk.Checkbutton(root, text="Search + Replace",
                   variable=search_replace_var).pack(pady=5)

    tk.Label(root, text="Before:").pack(pady=5)
    text_before = tk.Text(root, wrap=tk.WORD, height=10, width=40)
    text_before.pack(pady=10)
    text_before.tag_config("highlight", background="yellow")

    tk.Label(root, text="After:").pack(pady=5)
    text_after = tk.Text(root, wrap=tk.WORD, height=10, width=40)
    text_after.pack(pady=10)
    text_after.tag_config("highlight", background="yellow")

    tk.Button(root, text="Highlight", command=highlight_selection).pack(pady=5)
    tk.Button(root, text="Submit", command=on_submit).pack(pady=5)

    root.mainloop()


if __name__ == '__main__':
    main()
