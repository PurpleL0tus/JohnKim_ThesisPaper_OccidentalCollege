import tkinter as tk
import re


def main():
    root = tk.Tk()
    root.title("Regex Tool")

    # --- regex + replace inputs ---
    frame_inputs = tk.Frame(root)
    frame_inputs.pack(fill=tk.X, padx=10, pady=5)

    tk.Label(frame_inputs, text="Regex:").grid(row=0, column=0, sticky=tk.W)
    regex_entry = tk.Entry(frame_inputs, width=50)
    regex_entry.grid(row=0, column=1, padx=5, pady=2)

    replace_label = tk.Label(frame_inputs, text="Replace:")
    replace_entry = tk.Entry(frame_inputs, width=50)

    # --- mode checkboxes (mutually exclusive) ---
    validate_var = tk.BooleanVar(value=True)
    replace_var = tk.BooleanVar(value=False)

    def on_validate_checked():
        if validate_var.get():
            replace_var.set(False)
            replace_label.grid_remove()
            replace_entry.grid_remove()
        else:
            validate_var.set(True)  # keep at least one checked

    def on_replace_checked():
        if replace_var.get():
            validate_var.set(False)
            replace_label.grid(row=1, column=0, sticky=tk.W)
            replace_entry.grid(row=1, column=1, padx=5, pady=2)
        else:
            validate_var.set(True)
            replace_label.grid_remove()
            replace_entry.grid_remove()

    frame_mode = tk.Frame(root)
    frame_mode.pack(anchor=tk.W, padx=10)
    tk.Checkbutton(frame_mode, text="Search/Validate", variable=validate_var,
                   command=on_validate_checked).pack(side=tk.LEFT)
    tk.Checkbutton(frame_mode, text="Search + Replace", variable=replace_var,
                   command=on_replace_checked).pack(side=tk.LEFT)

    # --- text areas ---
    tk.Label(root, text="Before:").pack(anchor=tk.W, padx=10)
    text_before = tk.Text(root, wrap=tk.WORD, height=10, width=60)
    text_before.pack(padx=10, pady=(0, 5))
    text_before.tag_config("highlight", background="yellow")
    text_before.tag_config("match", background="lightgreen")

    tk.Label(root, text="After:").pack(anchor=tk.W, padx=10)
    text_after = tk.Text(root, wrap=tk.WORD, height=10, width=60)
    text_after.pack(padx=10, pady=(0, 5))
    text_after.tag_config("highlight", background="yellow")

    # --- buttons ---
    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=5)

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
            pass

    def on_submit():
        pattern = regex_entry.get().strip()
        input_text = text_before.get("1.0", tk.END).rstrip("\n")

        text_before.tag_remove("match", "1.0", tk.END)
        text_after.delete("1.0", tk.END)

        if not pattern:
            text_after.insert(tk.END, "Enter a regex pattern.")
            return

        try:
            compiled = re.compile(pattern)
        except re.error as e:
            text_after.insert(tk.END, f"Invalid regex: {e}")
            return

        if replace_var.get():
            result = compiled.sub(replace_entry.get(), input_text)
            text_after.insert(tk.END, result)
        else:
            matches = list(compiled.finditer(input_text))
            if not matches:
                text_after.insert(tk.END, "No matches found.")
                return

            for m in matches:
                text_before.tag_add("match", f"1.0+{m.start()}c", f"1.0+{m.end()}c")

            text_after.insert(tk.END, f"{len(matches)} match(es) found:\n\n")
            for i, m in enumerate(matches, 1):
                text_after.insert(tk.END, f"{i}. '{m.group()}' at pos {m.start()}–{m.end()}\n")

    tk.Button(frame_btn, text="Highlight", command=highlight_selection).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Submit", command=on_submit).pack(side=tk.LEFT, padx=5)

    root.mainloop()


if __name__ == '__main__':
    main()
