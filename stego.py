import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import pygame
import steg_utils
import subprocess
import sys
import secrets
import string
class StegApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FINAL STEGANOGRAPHY PROJECT")
        self.root.geometry("1180x680")  
        self.root.configure(bg="#0b0b0b")
        pygame.mixer.init()
        self.path = ""
        self.actual_message = ""
        self.show_msg_state = False
        self.show_pwd_state = False
        self.is_toggling = False  
        self.is_paused = False 
        self.accent_green = "#14ebaa"
        self.accent_purple = "#b69bf1"
        self.accent_cyan = "#10d3da"
        self.panel_bg = "#1f1f23"
        self.input_bg = "#2d2d34"
        self.text_white = "#ffffff"
        self.text_gray = "#8e8e93"
        tk.Label(root, text="FINAL STEGANOGRAPHY PROJECT",font=("Helvetica", 24, "bold"),bg="#0b0b0b", fg=self.text_white).pack(pady=(20, 20))
        upper_row = tk.Frame(root, bg="#0b0b0b")
        upper_row.pack(fill="x", padx=40)
        msg_container = tk.Frame(upper_row, bg="#0b0b0b")
        msg_container.pack(side="left", fill="both", expand=True, padx=(0, 15))
        tk.Label(msg_container, text="Secret Message", font=("Arial", 11, "bold"), bg="#0b0b0b", fg=self.text_white).pack(anchor="w", pady=(0, 6))
        left_panel = tk.Frame(msg_container, bg=self.panel_bg, bd=0)
        left_panel.pack(fill="both", expand=True, ipady=15)
        input_wrapper = tk.Frame(left_panel, bg=self.input_bg)
        input_wrapper.pack(fill="x", padx=25, pady=(20, 15))
        self.msg_entry = tk.Text(input_wrapper, bg=self.input_bg, fg=self.text_white, insertbackground="white", font=("Consolas", 11), relief="flat", wrap="word", height=6)
        self.msg_entry.pack(side="left", fill="both", expand=True, padx=(15, 5), pady=12)
        self.msg_entry.bind("<Key>", self.mask_message_input)
        self.msg_eye = tk.Canvas(input_wrapper, width=25, height=20, bg=self.input_bg, highlightthickness=0, cursor="hand2")
        self.msg_eye.pack(side="right", padx=(5, 15))
        self.msg_eye.bind("<Button-1>", lambda e: self.toggle_msg_visibility())
        self.draw_eye_icon(self.msg_eye, visible=False)
        btn_frame = tk.Frame(left_panel, bg=self.panel_bg)
        btn_frame.pack(fill="x", padx=25, pady=(5, 5))
        tk.Button(btn_frame, text="Hide In Image", font=("Arial", 10, "bold"), bg=self.accent_green, fg="#121212", relief="flat", command=self.encode_image_file, cursor="hand2", width=14, height=2).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Hide In Video/Audio", font=("Arial", 10, "bold"), bg=self.accent_purple, fg="#121212", relief="flat", command=self.encode_video_file, cursor="hand2", width=18, height=2).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Extract Message", font=("Arial", 10, "bold"), bg=self.accent_cyan, fg="#121212", relief="flat", command=self.decode_any_file, cursor="hand2", width=15, height=2).pack(side="left", padx=10)
        media_container = tk.Frame(upper_row, bg="#0b0b0b")
        media_container.pack(side="right", fill="both", expand=True, padx=(15, 0))
        tk.Label(media_container, text="Media Carrier Source", font=("Arial", 11, "bold"), bg="#0b0b0b", fg=self.text_white).pack(anchor="w", pady=(0, 6))
        right_panel = tk.Frame(media_container, bg=self.panel_bg, bd=0)
        right_panel.pack(fill="both", expand=True, ipady=15)
        self.status = tk.Label(right_panel, text="No Carrier File Selected", font=("Arial", 11), bg=self.panel_bg, fg=self.text_gray, wraplength=400, justify="center")
        self.status.pack(pady=(80, 5), fill="x", padx=15)
        self.image_label = tk.Label(right_panel, bg=self.panel_bg)
        self.image_label.pack(pady=5)
        self.audio_frame = tk.Frame(right_panel, bg=self.panel_bg)
        self.audio_frame.pack(pady=5)
        self.play_btn = tk.Button(self.audio_frame, text="▶ Play", font=("Arial", 8, "bold"), bg="#4CAF50", fg="white", width=7, command=self.play_audio, relief="flat")
        self.pause_btn = tk.Button(self.audio_frame, text="⏸ Pause", font=("Arial", 8, "bold"), bg="#FF9800", fg="white", width=7, command=self.pause_audio, relief="flat")
        self.stop_btn = tk.Button(self.audio_frame, text="⏹ Stop", font=("Arial", 8, "bold"), bg="#f44336", fg="white", width=7, command=self.stop_audio, relief="flat")
        self.browse_btn = tk.Button(right_panel, text=" Browse & Select File", font=("Arial", 10, "bold"), bg=self.accent_cyan, fg="#121212", relief="flat", command=self.load_file, cursor="hand2", width=22, pady=6)
        self.browse_btn.pack(side="bottom", pady=(0, 15))
        bottom_container = tk.Frame(root, bg="#0b0b0b")
        bottom_container.pack(fill="x", padx=40, pady=(20, 0))
        bottom_container.columnconfigure(1, weight=1)
        inputs_frame = tk.Frame(bottom_container, bg="#0b0b0b")
        inputs_frame.grid(row=0, column=0, sticky="nw")
        tk.Label(inputs_frame, text="Private Key Password", bg="#0b0b0b", fg=self.text_white).pack(anchor="w")
        pwd_wrap1 = tk.Frame(inputs_frame, bg="#0b0b0b")
        pwd_wrap1.pack(anchor="w", pady=(5, 10))
        self.private_key_entry = tk.Entry(pwd_wrap1, show="*", bg=self.input_bg, fg=self.text_white, width=30)
        self.private_key_entry.pack(side="left")
        self.create_pwd_eye(pwd_wrap1, self.private_key_entry).pack(side="left", padx=5)
        tk.Label(inputs_frame, text="Public Key Password", bg="#0b0b0b", fg=self.text_white).pack(anchor="w")
        pwd_wrap2 = tk.Frame(inputs_frame, bg="#0b0b0b")
        pwd_wrap2.pack(anchor="w", pady=(5, 10))
        self.image_password_entry = tk.Entry(pwd_wrap2, show="*", bg=self.input_bg, fg=self.text_white, width=30)
        self.image_password_entry.pack(side="left")
        self.image_password_entry.bind("<KeyRelease>", self.update_security_meter)
        self.create_pwd_eye(pwd_wrap2, self.image_password_entry).pack(side="left", padx=5)
        analysis_frame = tk.Frame(bottom_container, bg="#0b0b0b")
        analysis_frame.grid(row=0, column=1, sticky="nw", padx=(60, 0), pady=(25, 0))
        self.analysis_lbl = tk.Label(analysis_frame, text="Password Security Analysis:\nWaiting for security key string entry ....", font=("Arial", 10), bg=self.panel_bg, fg=self.text_white, justify="left", anchor="w")
        self.analysis_lbl.grid(row=0, column=0, padx=(0, 20)) 
        self.meter_bar = tk.Label(analysis_frame, text="░░░░░░░░░░   0%", font=("Consolas", 14, "bold"),  bg=self.panel_bg, fg="#3a3a3c")
        self.meter_bar.grid(row=0, column=1, sticky="w")
        self.gen_btn = tk.Button(pwd_wrap2, text="Generate", font=("Arial", 8), bg=self.accent_cyan, fg="#121212", relief="flat", command=lambda: self.generate_password_to_field(self.image_password_entry), cursor="hand2")
        self.gen_btn.pack(side="left", padx=10)
        self.gen_btn_priv = tk.Button(pwd_wrap1, text="Generate", font=("Arial", 8), bg=self.accent_green, fg="#121212", relief="flat", command=lambda: self.generate_password_to_field(self.private_key_entry), cursor="hand2")
        self.gen_btn_priv.pack(side="left", padx=10)
    def generate_password_to_field(self, entry_widget):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(16))
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, password)
        if entry_widget == self.image_password_entry:
            self.update_security_meter()
    def draw_eye_icon(self, canvas, visible=True):
        canvas.delete("all")
        color = self.accent_cyan if visible else "#7a7a7a"
        canvas.create_arc(2, 4, 23, 16, start=15, extent=150, style="arc", outline=color, width=2)
        canvas.create_arc(2, 4, 23, 16, start=195, extent=150, style="arc", outline=color, width=2)
        canvas.create_oval(10, 7, 15, 12, fill=color, outline="")
        if not visible:
            canvas.create_line(4, 3, 21, 17, fill="#ff453a", width=2)
    def toggle_msg_visibility(self):
        self.show_msg_state = not self.show_msg_state
        self.draw_eye_icon(self.msg_eye, self.show_msg_state)
        self.is_toggling = True  
        self.msg_entry.delete("1.0", tk.END)
        if self.show_msg_state:
            self.msg_entry.insert(tk.INSERT, self.actual_message)
        else:
            self.msg_entry.insert(tk.INSERT, "^" * len(self.actual_message))
        self.is_toggling = False
    def create_pwd_eye(self, parent, entry_widget):
        eye = tk.Canvas(parent, width=25, height=20, bg=self.panel_bg, highlightthickness=0, cursor="hand2")
        eye.visible = False
        eye.entry = entry_widget
        eye.bind("<Button-1>", lambda e: self.toggle_pwd_visibility(eye))
        self.draw_eye_icon(eye, visible=False)
        return eye
    def toggle_pwd_visibility(self,eye_canvas):
        eye_canvas.visible = not eye_canvas.visible
        self.draw_eye_icon(eye_canvas, eye_canvas.visible)
        eye_canvas.entry.config(show="" if eye_canvas.visible else "*")
    def mask_message_input(self, event):
        if self.is_toggling:
            return None  
        if event.keysym == "BackSpace":
            if len(self.actual_message) > 0:
                self.actual_message = self.actual_message[:-1]
            return None
        if event.keysym in ["Return", "Tab", "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Caps_Lock", "Escape"]:
            if event.keysym == "Return":
                self.actual_message += "\n"
            return None
        if event.char:
            self.actual_message += event.char
            self.msg_entry.insert(tk.INSERT, event.char if self.show_msg_state else "^")
            return "break"
    def update_security_meter(self, event=None):
        password = self.image_password_entry.get() 
        length = len(password)
        if length == 0:
            self.analysis_lbl.config(text="Password Security Analysis:\nWaiting for security key string entry ....")
            self.meter_bar.config(text="░░░░░░░░░░   0%", fg="#3a3a3c")
            return
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_spec = any(not c.isalnum() for c in password)
        score = min(4, int(length / 3))
        if has_upper and has_lower: score += 1
        if has_digit: score += 1
        if has_spec: score += 1
        meter_pct = min(100, int((score / 7) * 100))
        if meter_pct < 40:
            rating, color, bar_chars = "LOW", "#ff453a", "████░░░░░░"
        elif meter_pct < 75:
            rating, color, bar_chars = "MEDIUM", "#ff9f0a", "███████░░░"
        else:
            rating, color, bar_chars = "HIGH", self.accent_green, "██████████"
        self.analysis_lbl.config(text=f"Password Security Analysis\nLength: {length} characters  |  Encryption: AES-256 + RSA-2048\nEstimated Security: {rating}")
        self.meter_bar.config(text=f"{bar_chars}   {meter_pct}%", fg=color)
    def create_placeholder_icon(self, file_type):
        img = Image.new("RGBA", (130, 130), (31, 31, 35, 255))
        draw = ImageDraw.Draw(img)
        if file_type == "audio":
            draw.ellipse([30, 85, 60, 110], fill=(214, 155, 241, 255))
            draw.ellipse([75, 75, 105, 100], fill=(214, 155, 241, 255))
            draw.rectangle([55, 40, 60, 100], fill=(214, 155, 241, 255))
            draw.rectangle([100, 30, 105, 90], fill=(214, 155, 241, 255))
            draw.polygon([(55, 40), (100, 30), (100, 50), (55, 60)], fill=(214, 155, 241, 255))
        elif file_type == "video":
            draw.rectangle([25, 45, 105, 95], fill=(16, 211, 218, 255))
            draw.polygon([(30, 30), (50, 30), (40, 45), (25, 45)], fill=(255, 255, 255, 255))
            draw.polygon([(60, 30), (80, 30), (70, 45), (50, 45)], fill=(255, 255, 255, 255))
            draw.rectangle([25, 42, 105, 45], fill=(255, 255, 255, 255))
        else:
            draw.rectangle([40, 25, 90, 105], fill=(255, 255, 255, 255))
            draw.polygon([(75, 25), (90, 25), (75, 40)], fill=(200, 200, 200, 255))
        return ImageTk.PhotoImage(img)
    def load_file(self):
        chosen_path = filedialog.askopenfilename(
            filetypes=[("All Supported Files", "*.png *.jpg *.jpeg *.bmp *.mp3 *.mp2 *.wav *.m4a *.flac *.mp4 *.mkv *.avi *.mov"),
                       ("Images", "*.png *.jpg *.jpeg *.bmp"),
                       ("Audio Files", "*.mp3 *.mp2 *.wav *.m4a *.flac"),
                       ("Video Files", "*.mp4 *.mkv *.avi *.mov")]
        )
        if not chosen_path: 
            return
          
        if not os.path.exists(chosen_path):
            messagebox.showerror("Error", "File not found")
            return
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except:
            pass
        self.path = chosen_path
        ext = os.path.splitext(self.path)[1].lower()
        self.status.config(text=f"Loaded: {os.path.basename(self.path)}", fg=self.accent_cyan)
        self.play_btn.pack_forget()
        self.pause_btn.pack_forget()
        self.stop_btn.pack_forget()
        if ext in [".png", ".jpg", ".jpeg", ".bmp"]:
            try:
                self.status.config(text="")
                img = Image.open(self.path).resize((130, 130))
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo
            except:
                self.image_label.config(image="", text="⚠️ Preview Error", font=("Arial", 12), fg="orange")
        elif ext in [".mp3", ".mp2", ".wav", ".m4a", ".flac"]: 
            photo = self.create_placeholder_icon("audio")
            self.image_label.config(image=photo, text="Audio File Track Ready", font=("Arial", 11, "bold"), fg=self.accent_purple, compound="top")
            self.image_label.image = photo
            self.play_btn.pack(side="left", padx=4)
            self.pause_btn.pack(side="left", padx=4)
            self.stop_btn.pack(side="left", padx=4)
            try: 
                pygame.mixer.music.load(self.path)
            except: 
                pass
        elif ext in [".mp4", ".mkv", ".avi", ".mov"]:
            photo = self.create_placeholder_icon("video")
            self.image_label.config(image=photo, text="Video File Frame Ready", font=("Arial", 11, "bold"), fg=self.accent_cyan, compound="top")
            self.image_label.image = photo
        else:
            photo = self.create_placeholder_icon("document")
            self.image_label.config(image=photo, text="Document Carrier Active", font=("Arial", 11, "bold"), fg=self.text_white, compound="top")
            self.image_label.image = photo
    def play_audio(self):
        if self.path and os.path.exists(self.path):
            try:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(self.path)
                pygame.mixer.music.play()
                self.is_paused = False 
                self.status.config(text="Playing audio track...", fg=self.accent_green)
            except Exception as e:
                try:
                    if sys.platform == "win32":
                        os.startfile(self.path)
                    elif sys.platform == "darwin":
                        subprocess.call(["open", self.path])
                    else:
                        subprocess.call(["xdg-open", self.path])
                    self.status.config(text="Playing audio in default system player...", fg=self.accent_green)
                except:
                    self.status.config(text="⚠️ Playback codec error", fg="orange")
    def pause_audio(self):
        try:
            if not self.is_paused:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.status.config(text="Audio playback paused.", fg=self.text_gray)
            else:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.status.config(text="Playing audio track...", fg=self.accent_green)
        except:
            pass
    def stop_audio(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.is_paused = False 
            self.status.config(text="Audio track stopped.", fg=self.text_gray)
        except:
            pass
    def encode_image_file(self):
        if not self.path:
            messagebox.showerror("Error", "Select source file first!")
            return
        secret = self.actual_message.strip()
        private_key_password = self.private_key_entry.get().strip()
        image_password = self.image_password_entry.get().strip()
        if not secret or not private_key_password or not image_password:
            messagebox.showerror("Error", "Message and password required")
            return
        save_path = filedialog.asksaveasfilename(
            title="Save Encoded Image",
            defaultextension=".png", 
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg *.jpeg")]
        )
        if save_path:
            try:
                steg_utils.hide_in_image(self.path, save_path, secret, image_password,private_key_password)
                self.clear_fields("Successfully Encrypted & Hidden in Image!")
            except Exception as e:
                messagebox.showerror("Encryption Error", str(e))
    def encode_video_file(self):
        if not self.path:
            messagebox.showerror("Error", "Select source file first!")
            return
        secret = self.actual_message.strip()
        private_key_password = self.private_key_entry.get().strip()
        image_password = self.image_password_entry.get().strip()
        if not secret or not private_key_password or not image_password:
            messagebox.showerror("Error", "Message and password required")
            return
        save_path = filedialog.asksaveasfilename(
            title="Save Encoded Media",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4"),("MKV Video", "*.mkv"),("AVI Video", "*.avi"),("MOV Video", "*.mov"),("MP3 Audio", "*.mp3"), ("MP2 Audio", "*.mp2"), ("WAV Audio", "*.wav"), ("All Files", "*.*")])
        if save_path:
            try:
                self.stop_audio()
                steg_utils.hide_in_file_eof(self.path, save_path, secret, image_password, private_key_password)
                self.clear_fields("Successfully Encrypted & Hidden in Media!")
            except Exception as e:
                messagebox.showerror("Encryption Error", str(e))
    def decode_any_file(self):
        if not self.path:
            messagebox.showerror("Error", "Please select an encoded file first.")
            return
        private_key_password = self.private_key_entry.get().strip()  
        image_password = self.image_password_entry.get().strip()
        if not private_key_password or not image_password:
            messagebox.showerror("Error", "Password is required for decryption.")
            return 
        try:
            decoded_msg = steg_utils.extract_from_any(self.path, image_password, private_key_password)
            self.status.config(text="Decryption Successful!", fg=self.accent_green)
            self.msg_entry.delete("1.0", tk.END)
            self.msg_entry.insert(tk.INSERT, decoded_msg)
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt (Check Password):\n{str(e)}")
    def clear_fields(self, success_msg):
        self.status.config(text=success_msg, fg=self.accent_green)
        self.actual_message = ""
        self.msg_entry.delete("1.0", tk.END)
        self.private_key_entry.delete(0, tk.END)
        self.image_password_entry.delete(0, tk.END)
        self.update_security_meter()
if __name__ == "__main__":
    root = tk.Tk()
    app = StegApp(root)
    root.mainloop()