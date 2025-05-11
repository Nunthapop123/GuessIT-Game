import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib import colormaps
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class StatsUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Player Statistics")
        self.geometry("1366x1000")

        if os.path.exists("assets/data/game_log.csv"):
            self.level_df = pd.read_csv("assets/data/game_log.csv")
        else:
            self.level_df = pd.DataFrame()
        if os.path.exists("assets/data/game_summary.csv"):
            self.summary_df = pd.read_csv("assets/data/game_summary.csv")
        else:
            self.summary_df = pd.DataFrame()

        self.title_label = ctk.CTkLabel(self, text="📊 Visualization", font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=(10, 0))

        self.data_feature = ctk.CTkLabel(self, text="Data Feature:", font=("Helvetica", 18, "bold"))
        self.data_feature.pack(anchor="nw", pady=(10, 5), padx=20)

        description = (
            "• Player Score – Points earned per level.\n"
            "• Guess Accuracy – How close each guess was to the correct word.\n"
            "• Attempts Used – Number of tries before solving the word.\n"
            "• Power-Ups Used – Tracks which items were used.\n"
            "• Level Reached – Tracks which level player reached."
        )
        self.desc_label = ctk.CTkLabel(self, text=description, font=("Helvetica", 14), justify="left")
        self.desc_label.pack(pady=(5, 10), anchor="w", padx=20)

        self.selector_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.selector_frame.pack(anchor="nw", padx=20, pady=(0, 10))

        self.view_label = ctk.CTkLabel(self.selector_frame, text="Select Graph or Table", font=("Helvetica", 12))
        self.view_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.view_selector = ctk.CTkComboBox(
            self.selector_frame,
            values=["Graph", "Table"],
            command=self.on_view_change,
            width=120
        )
        self.view_selector.set("Graph")
        self.view_selector.grid(row=1, column=0, padx=(0, 10), pady=(0, 0))

        self.feature_label = ctk.CTkLabel(self.selector_frame, text="Select Attribute", font=("Helvetica", 12))
        self.feature_label.grid(row=0, column=1, sticky="w")
        self.feature_selector = ctk.CTkComboBox(
            self.selector_frame,
            values=["Player Score", "Guess Accuracy", "Power-Ups Used", "Level Reached"],
            command=self.update_view,
            width=200
        )
        self.feature_selector.set("Player Score")
        self.feature_selector.grid(row=1, column=1)

        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.update_view("Player Score")

    def on_view_change(self, view_type):
        if view_type == "Graph":
            self.feature_selector.configure(
                values=["Player Score", "Guess Accuracy", "Power-Ups Used", "Level Reached"]
            )
            self.feature_selector.set("Player Score")
        else:
            self.feature_selector.configure(
                values=["Player Score", "Attempts Used"]
            )
            self.feature_selector.set("Player Score")
        self.update_view(self.feature_selector.get())

    def update_view(self, selection):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        if self.view_selector.get() == "Graph":
            self.show_graph(selection)
        else:
            self.show_table(selection)

    def show_graph(self, selection):
        fig = plt.figure(figsize=(6, 4))

        if selection == "Player Score":
            ax = fig.add_subplot()
            ax.hist(self.level_df["Score"], bins=4, color='skyblue', edgecolor='black')
            ax.set_title("Distribution of Player Scores", fontsize=10)
            ax.set_xlabel("Score Range", fontsize=9)
            ax.set_ylabel("Frequency", fontsize=9)
            ax.tick_params(axis='both', labelsize=7)

        elif selection == "Guess Accuracy":
            grouped = self.level_df.groupby("Level")["Guess Accuracy"].mean().reset_index()
            ax = fig.add_subplot()
            ax.plot(grouped["Level"], grouped["Guess Accuracy"], marker='o', color='lightcoral')
            ax.set_title("Average Guess Accuracy Each Levels", fontsize=10)
            ax.set_xlabel("Level", fontsize=9)
            ax.set_ylabel("Average Accuracy", fontsize=9)
            ax.tick_params(axis='both', labelsize=7)

        elif selection == "Power-Ups Used":
            if "Bombs Used" in self.summary_df.columns and "Magnifies Used" in self.summary_df.columns:
                total_bombs = self.summary_df["Bombs Used"].sum()
                total_magnifies = self.summary_df["Magnifies Used"].sum()
                powerup_dict = {
                    "Bomb": int(total_bombs),
                    "Magnify": int(total_magnifies)
                }
                powerup_dict = {k: v for k, v in powerup_dict.items() if v > 0}
                if powerup_dict:
                    ax = fig.add_subplot()
                    cmap = colormaps.get_cmap("Set2")
                    colors = [cmap(i) for i in range(len(powerup_dict))]
                    ax.pie(powerup_dict.values(), labels=powerup_dict.keys(), autopct="%1.1f%%",
                           startangle=90, colors=colors, textprops={'fontsize': 9})
                    ax.set_title("Power-Ups Used Percentage", fontsize=10)

        elif selection == "Level Reached":
            if "Final Level" in self.summary_df.columns:
                level_counts = self.summary_df["Final Level"].value_counts().sort_index()
                ax = fig.add_subplot()
                num_levels = len(level_counts)
                cmap = colormaps.get_cmap('Set3')
                colors = [cmap(i / num_levels) for i in range(num_levels)]
                ax.bar(level_counts.index.astype(str), level_counts.values, color=colors)
                ax.set_title("Level Reached Distribution", fontsize=10)
                ax.set_xlabel("Level", fontsize=9)
                ax.set_ylabel("Count", fontsize=9)
                ax.set_yticks(range(0, max(level_counts.values) + 1))
                ax.tick_params(axis='both', labelsize=7)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_table(self, selection):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        if selection == "Player Score" and "Score" in self.level_df.columns:
            series = self.level_df["Score"]
            table_title = "Player Score Table"
        elif selection == "Attempts Used" and "Attempts Used" in self.level_df.columns:
            series = self.level_df["Attempts Used"]
            table_title = "Attempts Used Table"
        else:
            return

        stats = {
            "Mean": round(series.mean(), 2),
            "Median": round(series.median(), 2),
            "Standard Deviation": round(series.std(), 2),
            "Minimum": series.min(),
            "Maximum": series.max()
        }

        table_label = ctk.CTkLabel(self.graph_frame, text=table_title, font=("Helvetica", 18, "bold"))
        table_label.pack(pady=(10, 0))

        table_frame = ctk.CTkFrame(self.graph_frame)
        table_frame.pack(pady=20)

        header_font = ("Helvetica", 14, "bold")
        cell_font = ("Helvetica", 13)

        ctk.CTkLabel(table_frame, text="Metric", font=header_font, width=160).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(table_frame, text="Value", font=header_font, width=160).grid(row=0, column=1, padx=10, pady=5)

        for i, (key, value) in enumerate(stats.items(), start=1):
            ctk.CTkLabel(table_frame, text=key, font=cell_font).grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text=str(value), font=cell_font).grid(row=i, column=1, padx=10, pady=5)


if __name__ == "__main__":
    app = StatsUI()
    app.mainloop()