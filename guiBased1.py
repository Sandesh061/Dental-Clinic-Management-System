from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as tk
import cv2
import re
import db2
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import io
from io import BytesIO
from PIL import Image,ImageTk
import sys

class DentalClinic(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        db2.create_user_credentials_database()
        self.master = master
        self.master.title("Oral Eye")
        self.master.geometry("1850x900")
        logo_image = tk.PhotoImage(file=r".\Images\oral eye.png")  # Replace with the actual path to your logo file
        self.master.iconphoto(False, logo_image)
        # db2.create_database()
        # db2.create_user_credentials_database()
        self.signup_window=None
        self.dashboard_frame=None
        self.login_frame=None
        self.user_id=None
        self.create_widgets()
        
        self.content_frame=None
        self.nav_bar=None
        self.sidebar=None
        self.add_patient_window=None
        self.patient_form=None
        self.signup_window=None
        self.patient_form=None
        self.image_source_window=None
        self.image_options_frame=None
        self.Image_view=None
        self.capture_frame=None
        self.patient_form1=None
        self.patient_details_frame=None
        self.image_frame33=None
        self.final_diagnosis_entry=None
        self.sidebar=None
        self.list1=[]
        self.provisional_diagnosis_entry=None
        self.clinical_examination_entry=None
        self.treatment_plan_entry=None
        self.calculus=0
        # self.image_data2=None
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.image_window=None
        self.update_window=None
        self.last_selected_item = None
        # self.save_patient_and_choose_image_source(3)
        self.colors = master.style.colors
        self.pack(fill="both", expand=True)
        self.tree=None
        self.file_path_buccal=None
        self.file_path_maxilla=None
        self.file_path_mandible=None
        self.image_data1=None
        self.image_data2=None
        self.image_data4=None
        
        # self.save_patient_and_choose_image_source(1)
        
        # self.table=None
    def load_image(self,img_path):
        self.bg = Image.open(img_path)
        self.resized_bg = self.bg.resize((self.winfo_width(), self.winfo_height()))
        self.new_bg = ImageTk.PhotoImage(self.resized_bg)

        self.background_label = tk.Label(self.dashboard_frame, image=self.new_bg)
        self.background_label.place(relwidth=1, relheight=1)
    def load_image3(self,img_path):
        self.bg = Image.open(img_path)
        self.resized_bg = self.bg.resize((self.winfo_width(), self.winfo_height()))
        self.new_bg = ImageTk.PhotoImage(self.resized_bg)

        self.background_label = tk.Label(self.dashboard_frame, image=self.new_bg)
        self.background_label.place(relwidth=1, relheight=1)
    def resizer(self, event, image_path):
        # self.image_path = image_path  # Update the image path
        self.load_image(image_path)
        
    def load_image1(self, img_path):
        self.image_path = img_path  # Store the image path as an instance variable
        self.bg = Image.open(img_path)
        self.resized_bg = self.bg.resize((self.content_frame.winfo_width(), self.content_frame.winfo_height()))
        self.new_bg = ImageTk.PhotoImage(self.resized_bg)

        if hasattr(self, 'background_label'):
            # Update the existing label
            self.background_label.config(image=self.new_bg)
            self.background_label.image = self.new_bg
        else:
            # Create a new label
            self.background_label = tk.Label(self.dashboard_frame, image=self.new_bg)
            self.background_label.place(relwidth=1, relheight=1)
    def resizer4(self,event):
        x_=self.winfo_width()
        y_=self.winfo_height()
        new_x=50*x_/100
        new_y=50*y_/100
        x_=x_-new_x
        y_=y_-new_y
        new_x_enter_btn = x_  # You can adjust this value based on your needs
        new_y_enter_btn = y_
        self.login_frame.place(x=new_x_enter_btn, y=new_y_enter_btn)
    def resizer1(self, event,img_path):
        self.load_image1(img_path)
    def resizer2(self,event):
        x_=self.winfo_width()
        y_=self.winfo_height()
        new_x=41*x_/100
        new_y=23*y_/100
        x_=x_-new_x
        y_=y_-new_y
        new_x_enter_btn = x_  # You can adjust this value based on your needs
        new_y_enter_btn = y_  # You can adjust this value based on your needs

        self.enter_btn.place(x=new_x_enter_btn, y=new_y_enter_btn, height=50)
    def resizer3(self,event):
        if self.patient_form1:
            x_3=self.winfo_width()
            y_3=self.winfo_height()
            new_x3=64*x_3/100
            new_y3=80*y_3/100
            x_3=x_3-new_x3
            y_3=y_3-new_y3
            new_x_enter_btn3 = x_3  # You can adjust this value based on your needs
            new_y_enter_btn3 = y_3  # You can adjust this value based on your needs

            self.patient_form1.place(x=new_x_enter_btn3, y=new_y_enter_btn3)
        # return x_,y_ 
    def treatment_planGenerator(self,calculus, gingivitis):
        treatment_plan="Oral hygiene instruction to be provided"
        
        if calculus==1 and gingivitis==1:
            treatment_plan="Scaling and Root planning"
        elif calculus==0 and gingivitis==1:
            treatment_plan="Scaling"
        self.treatment_plan_entry.delete("1.0", "end")
        self.treatment_plan_entry.insert("1.0", treatment_plan)

    def Gingivitis_detection(self, patient_id, image_data_buccal, image_data_maxilla, image_data_mandible):
        custom_objects = {
            'input_shape': (256, 256, 3)
        }
        model1 = load_model(r'.\models\Color_Model.h5', custom_objects=custom_objects)
        model2 = load_model(r'.\models\Interdental_Papilla.h5', custom_objects=custom_objects)
        model3 = load_model(r'.\models\Contour.h5', custom_objects=custom_objects)
        model4 = load_model(r'.\models\Calculus.h5', custom_objects=custom_objects)
        
        try:
            # Convert image data to PIL Image
            img = Image.open(io.BytesIO(image_data_buccal))
            new_image = img.resize((256, 256))

            def predict(model, img, class_name):
                # warnings.filterwarnings("ignore", category=tf.RunningWithInferenceWarning)
                # warnings.filterwarnings("ignore", category=tf.function._SymbolicException)
                img_array = tf.keras.preprocessing.image.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)
                original_stdout = sys.stdout
                sys.stdout = open(os.devnull, 'w')
                predictions = model.predict(img_array)
                sys.stdout = original_stdout
                predicted_class = class_name[np.argmax(predictions[0])]
                return predicted_class

            pred1 = predict(model1, new_image, ['pink', 'red'])
            pred2= predict(model2, new_image, ['normal', 'swallon'])
            pred3= predict(model3, new_image, ['enlarged', 'not_enlarged'])
            pred4 = predict(model4, new_image, ['calculus_not_present', 'calculus_present'])
            self.image_data1=image_data_buccal
            self.image_data2=image_data_maxilla
            self.image_data4=image_data_mandible
            gingivitis = "No"

            if pred4 == 'calculus_not_present':
                self.calculus = 0
            else:
                self.calculus = 1

            if pred1 == 'red' or pred2 == 'swallon' or pred3 == 'enlarged' or pred4 == 'calculus_present':
                gingivitis = "Yes"

            if pred1=='red':
                pred1='Red or dark maroon with pigmentation'
            else:
                pred1='Coral pink with pigmentation'
            if pred2=='swallon':
                pred2='Reddish in color with enlargement'
            else:
                pred2='At the position/ coral pink in color'
            if pred3=='enlarged':
                pred3='Rolled gingival edges'
            else:
                pred3='Scalloped and knife edges'
            if pred4=='calculus_present':
                pred4='Present'
            else:
                pred4="Not present"
            clinical_examination_result = f"Color                   :  {pred1}\nInterdental Papilla :  {pred2}\nContour               :  {pred3}\nCalculus               :  {pred4}\n "
            if gingivitis=="Yes":
                provisional_diagnosis = "Chronic generalised gingivitis"
            else:
                provisional_diagnosis="Healthy Gingiva"

            self.clinical_examination_entry.delete("1.0", "end")
            self.clinical_examination_entry.insert("1.0", clinical_examination_result)
            self.provisional_diagnosis_entry.delete("1.0", "end")
            self.provisional_diagnosis_entry.insert("1.0", provisional_diagnosis)


        except Exception as e:
            messagebox.showerror("Error", f"Error in Gingivitis_detection: {str(e)}")
    
    def create_widgets(self):
        # Create a login frame
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
        if self.signup_window:
            self.signup_window.destroy()
        self.dashboard_frame = tk.Frame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        button_style = tk.Style()
        button_style.configure("Custom.TButton",background="#012342", font=("Arial", 14),borderwidth=0)
        img_path1 = r".\Images\1.png"
        self.load_image(img_path1)
        self.dashboard_frame.bind("<Configure>", lambda e, img_path=img_path1: self.resizer(e, img_path1))

        self.login_frame_style = tk.Style()
        self.login_frame_style.configure("Custom.TFrame", bootstyle="success")
        self.login_frame = ttk.Frame(self, style="Custom.TFrame")
        self.login_frame.pack(fill="both", expand=True)
        self.login_frame.place(in_=self, anchor="c", relx=0.52, rely=0.57, relheight=0.43, relwidth=0.33)

        style = ttk.Style()
        style.configure("Custom.TFrame", background="#7DF2DE")
        self.label = tk.Label(self.login_frame, text="        Login Your Account       ", style="TLabel", font=("Arial", 20),background="#012342", foreground="#ffffff")
        # self.label.config(fg="white")
        self.username_label = tk.Label(self.login_frame, text="    Username:", style="TLabel", font=("Arial", 18),background="#012342", foreground="#ffffff")
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        self.password_label = tk.Label(self.login_frame, text="    Password:", style="TLabel", font=("Arial", 18),background="#012342", foreground="#ffffff")
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 14))
        forget_password_label = tk.Label(self.login_frame, text="Forget Password?", style="TLabel", font=("Arial", 12), cursor="hand2",background="#7DF2DE", foreground="#00337C")
        forget_password_label.grid(row=3, column=1, pady=7, padx=30)
        forget_password_label.bind("<Button-1>", self.forget_password)
        self.login_button_style = tk.Style()
        self.login_button_style.configure("Custom.TButton", borderwidth=2, relief="ridge", font=("Arial", 15))
        self.login_button = tk.Button(self.login_frame, text=" Create Account ", command=lambda: (self.login_frame.destroy(), self.show_signup()), style="Custom.TButton",cursor="hand2")
        self.signup_button = tk.Button(self.login_frame, text=" Login ",command=self.login , style="Custom.TButton",cursor="hand2")

        self.label.grid(row=0, columnspan=2,padx=100, pady=40,sticky="nsew")
        self.username_label.grid(row=1, column=0, padx=50, pady=20, sticky="nsew")
        self.username_entry.grid(row=1, column=1, padx=2, pady=20)
        self.password_label.grid(row=2, column=0, padx=50, pady=20, sticky="nsew")
        self.password_entry.grid(row=2, column=1, padx=2, pady=20)
        self.login_button.grid(row=4, column=0, columnspan=1, pady=20, padx=10,sticky="e")
        self.signup_button.grid(row=4, column=1, pady=20, padx=10)  
        
    def forget_password(self,event):
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
        if self.login_frame:
            self.login_frame.destroy()
        self.dashboard_frame=tk.Frame(self)
        self.dashboard_frame.pack(fill="both",expand=True)
        img_path2=r".\Images\1.png"
        self.load_image(img_path2)
        self.dashboard_frame.bind("<Configure>", lambda e, img_path=img_path2: self.resizer(e, img_path2))
        self.login_frame_style = tk.Style()
        self.login_frame_style.configure("Custom.TFrame", bootstyle="success")
        self.signup_window = ttk.Frame(self, style="Custom.TFrame")
        self.signup_window.pack(fill="both", expand=True)
        self.signup_window.place(in_=self, anchor="c", relx=0.51, rely=0.566, relheight=0.43, relwidth=0.35)
        # relx=0.52, rely=0.57, relheight=0.43, relwidth=0.33
# Create a custom style with the desired background color
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#7DF2DE")
        self.label = tk.Label(self.signup_window, text="            Reset Password            ", style="TLabel",font=("Arial",20),background="#012342", foreground="#ffffff")
        self.new_username_label = tk.Label(self.signup_window, text=" Enter Username: " ,style="TLabel",font=("Arial",18),background="#012342", foreground="#ffffff")
        # self.new_username_label.pack()
        self.new_username_entry = tk.Entry(self.signup_window,font=("Arial",15))

        self.new_password_label = tk.Label(self.signup_window, text="  New Password:",style="TLabel",font=("Arial",18),background="#012342", foreground="#ffffff")
        # self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.signup_window, show="*",font=("Arial",15))
        # self.new_password_entry.pack()
        self.login_button_style = tk.Style()
        self.login_button_style.configure("Custom.TButton", borderwidth=2, relief="ridge", font=("Arial", 15))
        self.back_button = tk.Button(self.signup_window, text="Back", command=lambda:(self.signup_window.destroy(),self.create_widgets()), style="Custom.TButton",cursor="hand2")
        signup_button2 = tk.Button(self.signup_window, text="Save", command=self.Reset_password, style="Custom.TButton",cursor="hand2")
        # signup_button2.pack(pady=10)
        self.label.grid(row=0, columnspan=2, padx=100, pady=40, sticky="nsew")
        self.new_username_label.grid(row=1, column=0, padx=50, pady=20, sticky="nsew")
        self.new_username_entry.grid(row=1, column=1, padx=2, pady=20)
        self.new_password_label.grid(row=2, column=0, padx=50, pady=27, sticky="nsew")
        self.new_password_entry.grid(row=2, column=1, padx=2, pady=27)
        self.back_button.grid(row=3, column=0, columnspan=1, pady=40, padx=10)
        signup_button2.grid(row=3, column=1, pady=40, padx=10) 
        
    def Reset_password(self):
        username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        # if new_password=="":
        #     messagebox.showerror('Error','Password cannot be empty')
        is_present=db2.is_username_present(username)
        if is_present==False or new_password=="":
            messagebox.showerror('Error','Invalid Data')
        else:
            db2.update_password(username,new_password)
            self.signup_window.destroy()
            self.create_widgets()
    def show_signup(self):
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
        if self.login_frame:
            self.login_frame.destroy()
        self.dashboard_frame=tk.Frame(self)
        self.dashboard_frame.pack(fill="both",expand=True)
        img_path2=r".\Images\1.png"
        self.load_image(img_path2)
        self.dashboard_frame.bind("<Configure>", lambda e, img_path=img_path2: self.resizer(e, img_path2))
        self.login_frame_style = tk.Style()
        self.login_frame_style.configure("Custom.TFrame", bootstyle="success")
        self.signup_window = ttk.Frame(self, style="Custom.TFrame")
        self.signup_window.pack(fill="both", expand=True)
        self.signup_window.place(in_=self, anchor="c", relx=0.50, rely=0.566, relheight=0.43, relwidth=0.36)
        
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#7DF2DE")
        self.label = tk.Label(self.signup_window, text="          Create a new account          ", style="TLabel",font=("Arial",20),background="#012342", foreground="#ffffff")
        self.new_username_label = tk.Label(self.signup_window, text=" New Username: " ,style="TLabel",font=("Arial",18),background="#012342", foreground="#ffffff")
        # self.new_username_label.pack()
        self.new_username_entry = tk.Entry(self.signup_window,font=("Arial",15))

        self.new_password_label = tk.Label(self.signup_window, text="  New Password:",style="TLabel",font=("Arial",18),background="#012342", foreground="#ffffff")
        # self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.signup_window, show="*",font=("Arial",15))
        # self.new_password_entry.pack()
        self.login_button_style = tk.Style()
        self.login_button_style.configure("Custom.TButton", borderwidth=2, relief="ridge", font=("Arial", 15))
        self.back_button = tk.Button(self.signup_window, text="Back", command=lambda:(self.signup_window.destroy(),self.create_widgets()), style="Custom.TButton",cursor="hand2")
        signup_button2 = tk.Button(self.signup_window, text="Create Account", command=self.signup, style="Custom.TButton",cursor="hand2")
        # signup_button2.pack(pady=10)
        self.label.grid(row=0, columnspan=2, padx=100, pady=40, sticky="nsew")
        self.new_username_label.grid(row=1, column=0, padx=50, pady=20, sticky="nsew")
        self.new_username_entry.grid(row=1, column=1, padx=2, pady=20)
        self.new_password_label.grid(row=2, column=0, padx=50, pady=27, sticky="nsew")
        self.new_password_entry.grid(row=2, column=1, padx=2, pady=27)
        self.back_button.grid(row=3, column=0, columnspan=1, pady=40, padx=10)
        signup_button2.grid(row=3, column=1, pady=40, padx=10)
    def login(self):
        users_data=db2.get_all_users()
        primary_key=[]
        username1=[] 
        password1=[]
        # if not users_data:
        #     messagebox.showerror("Error","No users found")
        username = self.username_entry.get()
        password = self.password_entry.get()
        for user in users_data:
            primary_key.append(user[0])
            username1.append(user[1])
            password1.append(user[2])
        if username in username1 and password in password1:
            # self.user_id=user[0]
            index_user=username1.index(username)
            self.user_id=primary_key[index_user]
            db2.create_database(self.user_id)
            self.open_home()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
        
    def signup(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        if new_username=="":
            messagebox.showerror("Signup Failed","Invalid username or password")
            return
        users_data1=db2.get_all_users()
        username2=[]
        password2=[]
        for user in users_data1:
            username2.append(user[1])
            password2.append(user[2])
        # Check if the username already exists
        if new_username in username2:
            messagebox.showerror("Signup Failed", "Username already exists.")
        else:
            db2.insert_user(new_username,new_password)
            messagebox.showinfo("Signup Successful", "Your account has been created!")
            self.signup_window.destroy()
            self.create_widgets()
      
    def open_dashboard(self):
        self.close_window()
        button_style = tk.Style()
        button_style.configure("TButton", font=("Arial", 13), background="#4BC4A3",borderwidth=0)
        # Create a dashboard frame
        self.dashboard_frame = tk.Frame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        
        
        self.content_frame=tk.Frame(self.dashboard_frame)
        
        img_path1=r".\Images\2.png"
        self.load_image(img_path1)
        self.content_frame.bind("<Configure>", lambda e, img_path=img_path1: self.resizer1(e, img_path1))
        self.sidebar = tk.Frame(self.dashboard_frame, width=100,bootstyle="success")
        # self.sidebar.pack(side="left", fill="y")
        self.sidebar.place(x=0, y=0, relheight=1)
        

        # Create widgets for the sidebar using images
        patient_history_image = tk.PhotoImage(file=r".\Images\file2.png")
        add_patient_image = tk.PhotoImage(file=r".\Images\tooth2.png")
        # Resize the images (change the 2x2 to the desired size)
        patient_history_image = patient_history_image.subsample(2, 2)
        add_patient_image = add_patient_image.subsample(2, 2)

        
        add_patient_button = tk.Button(self.sidebar, image=add_patient_image,command=self.open_home)
        patient_history_button = tk.Button(self.sidebar, image=patient_history_image, command=self.show_patient_history)
        add_patient_button.image = add_patient_image
        patient_history_button.image = patient_history_image   
        add_patient_button.pack(pady=50)
        patient_history_button.pack()
        self.nav_bar = tk.Frame(self.dashboard_frame, bootstyle="white")
        self.nav_bar.place(x=100, y=0, relwidth=1, height=60)
        
        home_link = tk.Label(self.nav_bar, text="Home", cursor="hand2",font=("Arial",13),background="white")
        style = ttk.Style()
        style.configure("TLabel", foreground="Black")
        home_link.configure(style="TLabel")
        home_link.bind("<Button-1>", lambda event: self.open_home())
        home_link.pack(side="left", padx=20, pady=10)

        services_link = tk.Label(self.nav_bar, text="Services", cursor="hand2",font=("Arial",13), background="white",style="Custom_TLabel")
        services_link.bind("<Button-1>", lambda event: self.open_services())
        services_link.pack(side="left", padx=20)

        about_us_link = tk.Label(self.nav_bar, text="About Us", cursor="hand2", font=("Arial",13),background="white",style="Custom_TLabel")
        about_us_link.bind("<Button-1>", lambda event: self.open_about_us())
        about_us_link.pack(side="left", padx=20)

        contact_link = tk.Label(self.nav_bar, text="Contact", cursor="hand2", font=("Arial",13),background="white",style="Custom_TLabel")
        contact_link.bind("<Button-1>", lambda event: self.open_contact())
        contact_link.pack(side="left", padx=20)
        
        # Load user icon image
        user_icon_image = tk.PhotoImage(file=r".\Images\user.png")  # Replace with the path to your user icon image

        # Create a user menu
        self.user_menu = tk.Menu(self.nav_bar, tearoff=0,font=("Arial", 12))
        user1=db2.get_user_by_primary_key(self.user_id)
        user_name=user1[1]
        self.user_menu.add_command(label=user_name, state=tk.DISABLED,font=("Arial", 12))  # Replace with actual username
        self.user_menu.add_separator()
        self.user_menu.add_command(label="Sign Out", command=self.sign_out,font=("Arial", 12), foreground="red")

        # Create a label to display the user icon image
        user_button = tk.Label(self.nav_bar, image=user_icon_image, cursor="hand2")
        user_button.bind("<Button-1>", self.show_user_menu)
        user_button.image = user_icon_image
        user_button.pack(side="right", padx=250, pady=10)
        self.content_frame.pack(fill="both", expand=True)
    def show_user_menu(self,event):
        self.user_menu.post(event.x_root, event.y_root)
    def sign_out(self):
        self.close_window()
        self.create_widgets()
    def open_home(self):
        self.close_window()
        self.open_dashboard()
    def open_about_us(self):
        self.close_window()
        self.dashboard_frame = tk.Frame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        self.content_frame=tk.Frame(self.dashboard_frame)
        
        img_path1=r".\Images\contact.png"
        self.load_image(img_path1)
        self.content_frame.bind("<Configure>", lambda e, img_path=img_path1: self.resizer1(e, img_path1))
        self.sidebar = tk.Frame(self.dashboard_frame, width=100,bootstyle="success")
        # self.sidebar.pack(side="left", fill="y")
        self.sidebar.place(x=0, y=0, relheight=1)
        patient_history_image = tk.PhotoImage(file=r".\Images\file2.png")
        add_patient_image = tk.PhotoImage(file=r".\Images\tooth2.png")
        # Resize the images (change the 2x2 to the desired size)
        patient_history_image = patient_history_image.subsample(2, 2)
        add_patient_image = add_patient_image.subsample(2, 2)

        
        add_patient_button = tk.Button(self.sidebar, image=add_patient_image,command=self.open_home)
        patient_history_button = tk.Button(self.sidebar, image=patient_history_image, command=self.show_patient_history)
        add_patient_button.image = add_patient_image
        patient_history_button.image = patient_history_image   
        add_patient_button.pack(pady=50)
        patient_history_button.pack()
    
        about_us_text = """
                                            Welcome to Oral Eye!

    ⦿ At Oral Eye, we are passionate about delivering exceptional dental care and 
    innovative solutions to enhance your oral health.
    ⦿ We're dedicated to providing you the best of Healthcare, with a focus on 
    dependability and Oral disease diagnosis.
    ⦿ We're working to turn our passion for Healthcare in commiting to ensure 
    well-being and providing you with a comfortable and personalized experience.  


    Contact Information:
    - Contact No: 8296075475
    - Email: panshulkharche@gmail.com
    - Instagram: @panshulkharche

    Thank you for choosing Oral Eye. Your smile is our priority!
        """
        # self.attributes("-alpha", 0.7)
        self.enter_btn = tk.Frame(self.dashboard_frame, bootstyle="white")
        self.enter_btn.place(relx=0.24, rely=0.094)

        # Contact Information Section
        contact_info_label = tk.Label(self.enter_btn, text="  About Us  ", font=("Arial", 20, "bold"), background="#00E9BF")
        style = ttk.Style()
        style.configure("TLabel", foreground="#00337C")
        contact_info_label.configure(style="TLabel")
        contact_info_label.pack(side="top", padx=10, pady=30)

        contact_info_text = tk.Label(self.enter_btn, text=about_us_text, font=("Arial", 18), background="#00E9BF", justify="left")
        contact_info_text.configure(style="TLabel")
        contact_info_text.pack(side="left", padx=20, pady=30)  
        self.content_frame.pack(fill="both", expand=True)
    

    def open_services(self):
        self.close_window()
        self.dashboard_frame = tk.Frame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        self.content_frame=tk.Frame(self.dashboard_frame)
        
        img_path1=r".\Images\3.png"
        self.load_image(img_path1)
        self.content_frame.bind("<Configure>", lambda e, img_path=img_path1: self.resizer1(e, img_path1))
        self.sidebar = tk.Frame(self.dashboard_frame, width=100,bootstyle="success")
        # self.sidebar.pack(side="left", fill="y")
        self.sidebar.place(x=0, y=0, relheight=1)
        patient_history_image = tk.PhotoImage(file=r".\Images\file2.png")
        add_patient_image = tk.PhotoImage(file=r".\Images\tooth2.png")
        # Resize the images (change the 2x2 to the desired size)
        patient_history_image = patient_history_image.subsample(2, 2)
        add_patient_image = add_patient_image.subsample(2, 2)

        
        add_patient_button = tk.Button(self.sidebar, image=add_patient_image,command=self.open_home)
        patient_history_button = tk.Button(self.sidebar, image=patient_history_image, command=self.show_patient_history)
        add_patient_button.image = add_patient_image
        patient_history_button.image = patient_history_image   
        add_patient_button.pack(pady=50)
        patient_history_button.pack()
        
        self.enter_btn = tk.Frame(self.dashboard_frame, bootstyle="white")
        X_=self.winfo_width()
        Y_=self.winfo_height()
        new_x1=41*X_/100
        new_y1=23*Y_/100
        X_=X_-new_x1
        Y_=Y_-new_y1
        self.enter_btn.place(x=X_, y=Y_, height=50)
        
        home_link = tk.Label(self.enter_btn, text=" Enter➣ ", cursor="hand2",font=("Arial",14),background="#00E9BF")
        style = ttk.Style()
        style.configure("TLabel", foreground="white")
        home_link.configure(style="TLabel")
        home_link.bind("<Button-1>", lambda event: self.add_patient())
        home_link.pack(side="left", padx=1, pady=1)
        self.bind("<Configure>", self.resizer2)
        
        self.content_frame.pack(fill="both", expand=True)
    
    
    def image_button_clicked(self, patient_id):
        if self.patient_details_frame:
            self.patient_details_frame.destroy()
        if self.image_frame33:
            self.image_frame33.destroy()
        self.patient_details_frame = tk.Frame(self.dashboard_frame, bootstyle="white")
        self.patient_details_frame.place(relx=0.3, rely=0.03, relwidth=0.6, relheight=0.9)
        patient_details = db2.get_patient(patient_id, self.user_id)
        diagnosis_detail = db2.get_diagnosis2_records(patient_id,self.user_id)

        # Create labels for displaying patient details
        back_button = tk.Button(self.patient_details_frame, text=" ◀Back ", command=lambda: (self.patient_details_frame.destroy(), self.image_frame33.destroy()))
        # back_button.grid(row=0, column=1, padx=60, pady=10, sticky="nw")
        back_button.place(relx=0.95, rely=0.03, anchor="ne")
        
        label_style = tk.Style()
        label_style.configure("Custom.TLabel", font=("Arial", 14,"bold"),foreground="Black")
        name_label = tk.Label(self.patient_details_frame, text=f"Name: {patient_details[2]}", font=("Arial", 16, "bold"), style="Custom.TLabel")
        id_label = tk.Label(self.patient_details_frame, text=f"Patient ID: {patient_id}         Date: {patient_details[1]}", font=("Arial", 16),style="Custom.TLabel")
        age_label = tk.Label(self.patient_details_frame, text=f"Age: {patient_details[3]}", font=("Arial", 16),style="Custom.TLabel")
        gender_label = tk.Label(self.patient_details_frame, text=f"Gender: {patient_details[4]}", font=("Arial", 16),style="Custom.TLabel")
        phone_label = tk.Label(self.patient_details_frame, text=f"Phone: {patient_details[5]}", font=("Arial", 16),style="Custom.TLabel")

        chief_complaint_label = tk.Label(self.patient_details_frame, text="Chief Complaint", font=("Arial", 14, "bold"),style="Custom.TLabel", anchor="w")
        clinical_examination_label = tk.Label(self.patient_details_frame, text="Clinical Examination", font=("Arial", 14, "bold"),style="Custom.TLabel", anchor="w")
        provisional_diagnosis_label = tk.Label(self.patient_details_frame, text="Provisional Diagnosis", font=("Arial", 14, "bold"),style="Custom.TLabel", anchor="w")
        final_diagnosis_label = tk.Label(self.patient_details_frame, text="Final Diagnosis", font=("Arial", 14, "bold"),style="Custom.TLabel", anchor="w")
        treatment_plan_label = tk.Label(self.patient_details_frame, text="Treatment Plan", font=("Arial", 14, "bold"),style="Custom.TLabel", anchor="w")

        # Create text boxes
        chief_complaint_text = tk.Text(self.patient_details_frame, font=("Arial", 13), width=35, height=1)
        chief_complaint_text.insert(tk.END, diagnosis_detail[0][2])
        
        clinical_examination_text = tk.Text(self.patient_details_frame, font=("Arial", 13), width=46, height=4)
        clinical_examination_text.insert(tk.END, diagnosis_detail[0][3])
        
        provisional_diagnosis_text = tk.Text(self.patient_details_frame, font=("Arial", 13), width=35, height=1)
        provisional_diagnosis_text.insert(tk.END, diagnosis_detail[0][4])
        final_diagnosis_text = tk.Text(self.patient_details_frame, font=("Arial", 13), width=35, height=1)
        final_diagnosis_text.insert(tk.END, diagnosis_detail[0][5])
        treatment_plan_text = tk.Text(self.patient_details_frame, font=("Arial", 13), width=35, height=1)
        treatment_plan_text.insert(tk.END, diagnosis_detail[0][6])
        
        # Pack the labels and text boxes
        name_label.grid(row=0, column=0, padx=350, pady=8, sticky="w")
        id_label.grid(row=1, column=0, padx=250, pady=8, sticky="w")
        age_label.grid(row=2, column=0, padx=250, pady=8, sticky="w")
        gender_label.grid(row=3, column=0, padx=250, pady=8, sticky="w")
        phone_label.grid(row=4, column=0, padx=250, pady=8, sticky="w")
        
        chief_complaint_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        chief_complaint_text.grid(row=6, column=0, padx=20, pady=10, columnspan=2, sticky="w")
        
        clinical_examination_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        clinical_examination_text.grid(row=8, column=0, padx=20, pady=10, columnspan=2, sticky="w")
        
        provisional_diagnosis_label.grid(row=9, column=0, padx=20, pady=10, sticky="w")
        provisional_diagnosis_text.grid(row=10, column=0, padx=20, pady=10, columnspan=2, sticky="w")
        final_diagnosis_label.grid(row=11, column=0, padx=20, pady=10, sticky="w")
        final_diagnosis_text.grid(row=12, column=0, padx=20, pady=10, columnspan=2, sticky="w")
        treatment_plan_label.grid(row=13, column=0, padx=20, pady=10, sticky="w")
        treatment_plan_text.grid(row=14, column=0, padx=20, pady=10, columnspan=2, sticky="w")
        # Create a new frame for displaying the patient's image
        self.image_frame33 = tk.Frame(self.dashboard_frame, bootstyle="white")
        # self.image_frame33.place(relx=0.63, rely=0.30,relwidth=0.35, relheight=0.55)
        self.image_frame33.place(relx=0.63, rely=0.28)
        image_data=db2.get_image_data(patient_id,self.user_id)
        image_labels = ["Buccal", "Maxilla", "Mandible"]
        if image_data:
            # image_data2 = BytesIO(image_data)
            # image = tk.PhotoImage(data=image_data2.read())
            # # Create a label or canvas to display the image
            # image_label = tk.Label(self.image_frame33, image=image)
            # image_label.image = image  # To prevent garbage collection

            # # Place the label or canvas as needed
            # image_label.pack(fill="both", expand=True) 
            
            for idx, (img_data, label) in enumerate(zip(image_data, image_labels)):
                image_data2 = BytesIO(img_data)
                image = Image.open(image_data2)
                image = image.resize((300, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                row = idx // 2
                col = idx % 2
                
                section_frame = tk.Frame(self.image_frame33, relief="groove")
                section_frame.grid(row=row, column=col, padx=10, pady=10)
                
                section_label = tk.Label(section_frame, text=label, style="Custom.TLabel")
                section_label.pack(pady=3)
                
                image_label = tk.Label(section_frame, image=photo, background="white")
                image_label.image = photo  # To prevent garbage collection
                image_label.pack(padx=2,pady=10)
        delete_button = tk.Button(self.image_frame33, text=" Delete ", command=lambda: (self.delete_patient_record(patient_id)))
        delete_button.grid(row=3, column=1, padx=0, pady=10,sticky="w")
    
      
    def show_patient_history(self):
        
        global tree
        self.close_window()
        self.dashboard_frame = tk.Frame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        self.content_frame=tk.Frame(self.dashboard_frame)
        img_path4=r".\Images\62.png"
        self.load_image(img_path4)
        self.content_frame.bind("<Configure>", lambda e, img_path=img_path4: self.resizer1(e, img_path4))
        self.sidebar = tk.Frame(self.dashboard_frame, width=100,bootstyle="success")
        # self.sidebar.pack(side="left", fill="y")
        self.sidebar.place(x=0, y=0, relheight=1)
        patient_history_image = tk.PhotoImage(file=r".\Images\file2.png")
        add_patient_image = tk.PhotoImage(file=r".\Images\tooth2.png")
        # Resize the images (change the 2x2 to the desired size)
        patient_history_image = patient_history_image.subsample(2, 2)
        add_patient_image = add_patient_image.subsample(2, 2)
        add_patient_button = tk.Button(self.sidebar, image=add_patient_image,command=self.open_home)
        patient_history_button = tk.Button(self.sidebar, image=patient_history_image, command=self.show_patient_history)
        add_patient_button.image = add_patient_image
        patient_history_button.image = patient_history_image   
        add_patient_button.pack(pady=50)
        patient_history_button.pack()
        
        self.history_window = tk.Frame(self.dashboard_frame,bootstyle="success")
        self.history_window.place(relx=0.029, rely=0.088,relheight=0.89)

        style = tk.Style()
        style.configure("Custom.Treeview.Heading", font=("Arial", 16),background="#4BC4A3")
        style.configure("Custom.Treeview", font=("Arial", 14, "bold"), rowheight=30,borderwidth=0)
        # ,background="#4BC4A3"
        self.tree = tk.Treeview(self.history_window,style=("Custom.Treeview"), columns=("ID","Name", "Button"),  show="headings")
        
        vsb = tk.Scrollbar(self.history_window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y") 
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        self.tree.heading("#1", text="ID", anchor="center")
        self.tree.heading("#2", text="Name", anchor="center")  

        self.tree.column("#1", width=80, anchor="center")
        self.tree.column("#2", width=240,anchor="center")
        self.tree.column("#3", width=100,anchor="center")
        patientss = db2.get_all_patients(self.user_id)
        for i, patient in enumerate(patientss):
            
            record_tag = f"tag{i}"
            background_color = "white"

            # Configure tags
            self.tree.tag_configure(record_tag, background=background_color)

            # Insert the record row
            self.tree.insert("", "end", values=(patient[0], patient[2], "Open➤"), tags=(record_tag))

            self.tree.insert("", "end", values=("", "", ""), tags=("empty_row"))
        self.tree.tag_configure("empty_row", background="#4BC4A3")

        self.tree.bind("<ButtonRelease-1>", self.on_item_click)
        self.content_frame.pack(fill="both", expand=True)

    def open_contact(self):
        self.close_window()
        self.dashboard_frame = tk.Frame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        self.content_frame=tk.Frame(self.dashboard_frame)
        
        img_path1=r".\Images\contact.png"
        self.load_image(img_path1)
        self.content_frame.bind("<Configure>", lambda e, img_path=img_path1: self.resizer1(e, img_path1))
        self.sidebar = tk.Frame(self.dashboard_frame, width=100,bootstyle="success")
        self.sidebar.place(x=0, y=0, relheight=1)
        patient_history_image = tk.PhotoImage(file=r".\Images\file2.png")
        add_patient_image = tk.PhotoImage(file=r".\Images\tooth2.png")
        patient_history_image = patient_history_image.subsample(2, 2)
        add_patient_image = add_patient_image.subsample(2, 2)

        
        add_patient_button = tk.Button(self.sidebar, image=add_patient_image,command=self.open_home)
        patient_history_button = tk.Button(self.sidebar, image=patient_history_image, command=self.show_patient_history)
        add_patient_button.image = add_patient_image
        patient_history_button.image = patient_history_image   
        add_patient_button.pack(pady=50)
        patient_history_button.pack() 
        
        self.enter_btn = tk.Frame(self.dashboard_frame, bootstyle="white")
        self.enter_btn.place(relx=0.25, rely=0.2)

        # Contact Information Section
        contact_info_label = tk.Label(self.enter_btn, text="  Contact Us  ", font=("Arial", 20, "bold"), background="#00E9BF")
        style = ttk.Style()
        style.configure("TLabel", foreground="#00337C")
        contact_info_label.configure(style="TLabel")
        contact_info_label.pack(side="top", padx=10, pady=30)

        contact_info_text = tk.Label(self.enter_btn, text="\n     Address: Pansul Kharche, 1601-A, Yashwasin, Sai Developers, \n     Plot 38, Sec.27, Kharghar, Navi Mumbai, Maharashtra, 410210.    \n\n      Email: panshulkharche@gmail.com\n\n      Insta ID: @panshulkharche\n\n      Phone No: +918296075475\n", font=("Arial", 18), background="#00E9BF", justify="left")
        contact_info_text.configure(style="TLabel")
        contact_info_text.pack(side="left", padx=20, pady=30)

        

        self.content_frame.pack(fill="both", expand=True)
    def on_item_click(self,event):
        # global tree  
        selected_items = self.tree.selection()
        if not selected_items:
            return
        if "empty_row" in self.tree.item(selected_items, "tags"):
        # Do nothing for empty rows
            # self.tree.selection_remove(selected_items)
            if self.last_selected_item:
                self.tree.selection_set(self.last_selected_item)
            return
        item = selected_items[0]
        column = self.tree.identify_column(event.x)
        if column == "#3":
            patient_id = int(self.tree.item(item, "values")[0])
            self.image_button_clicked(patient_id)
        self.last_selected_item = selected_items
    def delete_patient_record(self,patient_id):
        confirm = messagebox.askyesno("Delete Patient", "Are you sure you want to delete this patient?")
        if confirm:
            if self.patient_details_frame:
                self.patient_details_frame.destroy()
            if self.image_frame33:
                self.image_frame33.destroy()
            db2.delete_patient(patient_id,self.user_id)
            # db2.delete_diagnosis(patient_id)
            db2.delete_dignosis2_record(patient_id,self.user_id)
            db2.delete_img(patient_id,self.user_id)
            self.tree.delete(*self.tree.get_children())
            self.show_patient_history()

    def add_patient(self):
        def is_valid_name(name):
            count=0
            count2=0
            for a in name:
                if(a.isspace()==True):
                    count+=1
                if a.isalpha():
                    count2 += 1
                if a.isdigit():
                    return False
            if count2>0 and count<4:
                # return name.isalpha()
                return True
            
            else:
                return False
        def submit():
            date=dob_entry.entry.get()
            name = name_entry.get()
            age = age_entry.get()
            gender = gender_var.get()
            # email = email_entry.get()
            phone = phone_entry.get()
            chief_complaint=complaint_entry.get("1.0", "end-1c")
            # You can add more fields as needed
            if not name or not age or not gender  or not phone:
                messagebox.showerror("Validation Error", "Please fill in all fields.")
                return
        
            if not name :
                messagebox.showerror("Validation Error", "Name is required and must contain only characters.")
                return
            if not is_valid_name(name):
                messagebox.showerror("Validation Error", "Name should contain only alphabetic characters.")
                return
            if not re.match(r"^\d{10}$", phone):
                messagebox.showerror("Validation Error", "Phone must be a 10-digit number.")
                return

            if gender not in ["Male", "Female", "Other"]:
                messagebox.showerror("Validation Error", "Please choose a valid gender from the dropdown.")
                return


            if not age.isdigit():
                messagebox.showerror("Validation Error", "Age must be a number.")
                return
            patients=db2.get_all_patients(self.user_id)
            if patients:
                patient_id = patients[len(patients) - 1][0]+1
            
            else:
                patient_id=1
        
            self.list1.append(date)
            self.list1.append(name)
            self.list1.append(age)
            self.list1.append(gender)
            self.list1.append(phone)
            self.list1.append(chief_complaint)
            self.close_window()
            self.save_patient_and_choose_image_source(patient_id)
        
        self.close_window()
        self.dashboard_frame = tk.Frame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        self.content_frame=tk.Frame(self.dashboard_frame)
        img_path2=r".\Images\4.png"
        self.load_image(img_path2)
        self.content_frame.bind("<Configure>", lambda e, img_path=img_path2: self.resizer1(e, img_path2))
        self.sidebar = tk.Frame(self.dashboard_frame, width=100,bootstyle="success")
        # self.sidebar.pack(side="left", fill="y")
        self.sidebar.place(x=0, y=0, relheight=1)
        patient_history_image = tk.PhotoImage(file=r".\Images\file2.png")
        add_patient_image = tk.PhotoImage(file=r".\Images\tooth2.png")
        # Resize the images (change the 2x2 to the desired size)
        patient_history_image = patient_history_image.subsample(2, 2)
        add_patient_image = add_patient_image.subsample(2, 2)
        add_patient_button = tk.Button(self.sidebar, image=add_patient_image,command=self.open_home)
        patient_history_button = tk.Button(self.sidebar, image=patient_history_image, command=self.show_patient_history)
        add_patient_button.image = add_patient_image
        patient_history_button.image = patient_history_image   
        add_patient_button.pack(pady=50)
        patient_history_button.pack()
        self.patient_form1=tk.Frame(self.dashboard_frame, bootstyle="white")
        # self.patient_form1.pack(fill="both", expand=True)
        X_=self.winfo_width()
        Y_=self.winfo_height()
        new_x1=64*X_/100
        new_y1=80*Y_/100
        X_=X_-new_x1
        Y_=Y_-new_y1

        self.patient_form1.place(x=X_, y=Y_)
        
        label_style = tk.Style()
        label_style.configure("Custom.TLabel", font=("Arial", 14,"bold"),foreground="Black")
        dob_label = tk.Label(self.patient_form1, text="Select Date:", style="Custom.TLabel")
        dob_entry = tk.DateEntry(self.patient_form1, bootstyle="success",width=20 )
        name_label = tk.Label(self.patient_form1, text="Enter Name:", style="Custom.TLabel")
        name_entry = tk.Entry(self.patient_form1, font=("Arial", 13),width=20)
        age_label = tk.Label(self.patient_form1, text="Enter Age:", style="Custom.TLabel")
        age_entry = tk.Entry(self.patient_form1, font=("Arial", 13),width=20)
    
        gender_label = tk.Label(self.patient_form1, text="Select Gender:", style="Custom.TLabel")
        gender_var = tk.StringVar()
        gender_combo = tk.Combobox(self.patient_form1, textvariable=gender_var, values=["Male", "Female", "Other"], font=("Arial", 13))
    
    
        phone_label = tk.Label(self.patient_form1, text="Enter Phone No:", style="Custom.TLabel")
        phone_entry = tk.Entry(self.patient_form1, font=("Arial", 13))
        complaint_label = tk.Label(self.patient_form1, text="Chief Complaint:", style="Custom.TLabel")
        complaint_entry = tk.Text(self.patient_form1, font=("Arial", 13),  width=50, height=5)
        back_button = tk.Button(self.patient_form1, text="Back", command=lambda:(self.close_window(), self.open_services()), style="TButton")
        submit_button = tk.Button(self.patient_form1, text=" click for clinical Examination ", command=submit, style="TButton")
        
        dob_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        dob_entry.grid(row=1, column=0, padx=10, pady=5,sticky="nsew")
        name_label.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        name_entry.grid(row=3, column=0, padx=10, pady=5,sticky="nsew")
    
        age_label.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        age_entry.grid(row=3, column=1, padx=10, pady=5,sticky="nsew")
    
        gender_label.grid(row=4, column=1, padx=10, pady=5, sticky="nsew")
        gender_combo.grid(row=5, column=1, padx=10, pady=5,sticky="nsew")
    
        phone_label.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        phone_entry.grid(row=5, column=0, padx=10, pady=5,sticky="nsew")
        complaint_label.grid(row=7, column=0, padx=0, pady=10, sticky="nsew")
        complaint_entry.grid(row=8, column=0, padx=0, pady=10)
        submit_button.grid(row=9, column=0, columnspan=2,padx=40, pady=10,sticky="w")
        back_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        self.bind("<Configure>", self.resizer3)
        self.content_frame.pack(fill="both", expand=True)
        

        # back_button.place(x=293, y=362)
    def close_window(self):
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
        if self.content_frame:
            self.content_frame.destroy()
        if self.nav_bar:
            self.nav_bar.destroy()
        if self.add_patient_window:
            self.add_patient_window.destroy()
        if self.patient_form:
            self.patient_form.destroy()
        if self.login_frame:
            self.login_frame.destroy()
        if self.signup_window:
            self.signup_window.destroy()
        if self.patient_form:
            self.patient_form.destroy()
        if self.sidebar:
            self.sidebar.destroy()
        if self.image_source_window:
            self.image_source_window.destroy()
        if self.image_options_frame:
            self.image_options_frame.destroy()
        if self.Image_view:
            self.Image_view.destroy()
        if self.capture_frame:
            self.capture_frame.destroy()
        if self.patient_form1:
            self.patient_form1.destroy()
        if self.login_frame:
            self.login_frame.destroy()
    
    def save_patient_and_choose_image_source(self, patient_id):
        self.close_window()
        self.dashboard_frame = tk.Frame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        self.content_frame = tk.Frame(self.dashboard_frame)
        img_path3 = r".\Images\5.png"
        self.load_image(img_path3)
        self.content_frame.bind("<Configure>", lambda e, img_path=img_path3: self.resizer1(e, img_path3))
        self.sidebar = tk.Frame(self.dashboard_frame, width=100, bootstyle="success")
        self.sidebar.place(x=0, y=0, relheight=1)
        
        patient_history_image = tk.PhotoImage(file=r".\Images\file2.png")
        add_patient_image = tk.PhotoImage(file=r".\Images\tooth2.png")
        patient_history_image = patient_history_image.subsample(2, 2)
        add_patient_image = add_patient_image.subsample(2, 2)

        add_patient_button = tk.Button(self.sidebar, image=add_patient_image, command=self.open_home)
        patient_history_button = tk.Button(self.sidebar, image=patient_history_image, command=self.show_patient_history)
        add_patient_button.image = add_patient_image
        patient_history_button.image = patient_history_image
        add_patient_button.pack(pady=50)
        patient_history_button.pack()
        
        self.content_frame.pack(fill="both", expand=True)
        self.patient_form = tk.Frame(self.dashboard_frame)
        self.patient_form.place(relx=0.1, rely=0.2)
        label_style = ttk.Style()
        label_style.configure("Custom.TLabel", font=("Arial", 14, "bold"))

        clinical_examination_label = ttk.Label(self.patient_form, text="Clinical Examination:", style="Custom.TLabel")
        clinical_examination_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.clinical_examination_entry = tk.Text(self.patient_form, font=("Arial", 13), width=50, height=5)
        self.clinical_examination_entry.grid(row=2, column=0, padx=10, pady=10)
        
        provisional_diagnosis_label = ttk.Label(self.patient_form, text="Provisional diagnosis:", style="Custom.TLabel")
        provisional_diagnosis_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.provisional_diagnosis_entry = tk.Text(self.patient_form, font=("Arial", 13), width=50, height=2)
        self.provisional_diagnosis_entry.grid(row=4, column=0, padx=10, pady=10)

        final_diagnosis_label = ttk.Label(self.patient_form, text="Final diagnosis:", style="Custom.TLabel")
        final_diagnosis_label.grid(row=5, column=0, pady=5, padx=10, sticky="w")
        self.final_diagnosis_entry = tk.Text(self.patient_form, font=("Arial", 13), width=50, height=2)
        self.final_diagnosis_entry.grid(row=6, column=0, padx=10, pady=10)

        treatment_plan_label = ttk.Label(self.patient_form, text="Treatment plan:", style="Custom.TLabel")
        treatment_plan_label.grid(row=7, column=0, pady=5, padx=10, sticky="w")
        self.treatment_plan_entry = tk.Text(self.patient_form, font=("Arial", 13), width=50, height=2)
        self.treatment_plan_entry.grid(row=8, column=0, padx=10, pady=10)
        
        def Get_final_diagnosis():
            final_digno = self.final_diagnosis_entry.get("1.0", "end-1c").lower()
            final_diagnosis = 0
            if "chronic" in final_digno or "gingivitis" in final_digno or "generalised" in final_digno:
                final_diagnosis = 1
            elif "healthy" in final_digno or "no" in final_digno:
                final_diagnosis = 0
            self.treatment_planGenerator(self.calculus, final_diagnosis)
        
        def digno_valid():
            final_digno = self.final_diagnosis_entry.get("1.0", "end-1c")
            treat_plan = self.treatment_plan_entry.get("1.0", "end-1c")
            if final_digno == "" or treat_plan == "":
                messagebox.showerror("Validation Error", "please enter required fields")
                return
            else:
                self.save_data(patient_id, self.clinical_examination_entry.get("1.0", "end-1c"), self.provisional_diagnosis_entry.get("1.0", "end-1c"), self.final_diagnosis_entry.get("1.0", "end-1c"), self.treatment_plan_entry.get("1.0", "end-1c"), self.image_data1, self.image_data2, self.image_data4)
                self.close_window()
                self.open_home()
        
        save_button = tk.Button(self.patient_form, text="Save", command=lambda: digno_valid())
        save_button.grid(row=9, column=0, pady=17, padx=50, sticky="w")
        
        Treatment_plan_button = tk.Button(self.patient_form, text="Generate Treatment Plan", command=lambda: Get_final_diagnosis())
        Treatment_plan_button.grid(row=9, column=0, pady=17, padx=10)
        
        back_button = tk.Button(self.patient_form, text="Back", command=lambda: (self.close_window(), self.open_home()))
        back_button.grid(row=9, column=1, pady=17, padx=10)
        
        # Create a box for image options on the right upper corner
        self.image_options_frame = tk.Frame(self.dashboard_frame, bootstyle="light")
        # image_options_frame.grid(row=0, column=2, rowspan=6, padx=10, pady=100)
        self.image_options_frame.place(relx=0.6, rely=0.13)

        
        label_style.configure("Custom.TLabel", font=("Arial", 14, "bold"), background="white")
        # label = ttk.Label(self.image_options_frame, text="Choose image source:", style="Custom.TLabel")
        # label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        image_sections = ["maxilla", "mandible", "buccal"]
        self.image_entries = {}
        for idx, section in enumerate(image_sections):
            row = idx // 2
            col = idx % 2
            
            section_frame = tk.Frame(self.image_options_frame, relief="groove")
            section_frame.grid(row=row+1, column=col, padx=20, pady=20)
            
            section_label = ttk.Label(section_frame, text=f"{section.capitalize()}:", style="Custom.TLabel")
            section_label.pack(pady=85)
            
            self.image_entries[section] = {"uploaded": None, "capture": None, "frame": section_frame}
            
            upload_image = tk.PhotoImage(file=r".\Images\upload_img.png").subsample(2, 2)
            capture_image = tk.PhotoImage(file=r".\Images\capture_img.png").subsample(2, 2)
            
            upload_button = tk.Button(section_frame, image=upload_image, command=lambda s=section: self.upload_image(patient_id, s))
            capture_button = tk.Button(section_frame, image=capture_image, command=lambda s=section: self.open_camera_capture_window(patient_id, s))
            
            upload_button.image = upload_image
            capture_button.image = capture_image
            upload_button.pack(side="left", padx=60, pady=15)
            capture_button.pack(side="right", padx=60, pady=15)
        # # Save All button, initially disabled
        # self.save_all_button = tk.Button(self.image_options_frame, text="Save", state=tk.DISABLED, command=lambda: self.save_image(self.file_path_buccal,self.file_path_maxilla, self.file_path_lingual, self.file_path_mandible, patient_id))
        # # self.save_all_button.pack(pady=20)
        # self.save_all_button.grid(row=3, column=1, padx=0, pady=10,sticky="w")
        
    
    def save_data(self,id,clinic_exam, prov_diag, fin_diag, treat_plan, img_data1, img_data2, img_data4):
        db2.insert_patient(self.list1[0],self.list1[1],self.list1[2],self.list1[3],self.list1[4],self.user_id)
        db2.insert_diagnosis2(id,self.list1[5],clinic_exam,prov_diag,fin_diag,treat_plan,self.user_id)
        db2.save_image_to_db(id, img_data1, img_data2, img_data4, self.user_id)
        self.list1=[]
    def upload_image(self, patient_id, section):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            if section=="buccal":
                self.file_path_buccal=file_path
            
            elif section=="mandible":
                self.file_path_mandible=file_path
            elif section=="maxilla":
                self.file_path_maxilla=file_path
            section_frame = self.image_entries[section]["frame"]
            # for widget in section_frame.winfo_children():
            #     if isinstance(widget, tk.Label) and hasattr(widget, 'photo'):
            #         widget.destroy()
            # Clear the section frame
            for widget in section_frame.winfo_children():
                widget.destroy()
            # Add section label above the image
            # self.style = ttk.Style()
            # self.style.configure("Custom.TLabel", font=("Helvetica", 10))

            section_label = ttk.Label(section_frame, text=f"{section.capitalize()}:", style="Custom.TLabel")
            section_label.pack(pady=1)

            img = Image.open(file_path)
            img = img.resize((300, 200), Image.LANCZOS)  # Resize the image to 150x150 pixels
            photo = ImageTk.PhotoImage(img)
            image_label = tk.Label(section_frame, image=photo)
            image_label.photo = photo
            image_label.pack(padx=2,pady=10)

            reupload_button = tk.Button(section_frame, text="⟲", command=lambda: self.upload_image(patient_id, section))
            # save_button = tk.Button(section_frame, text="Save", command=lambda: self.save_image(file_path, patient_id))
            # reupload_button.pack(side="left", padx=5, pady=5)
            reupload_button.pack(pady=5)
            # Save All button, initially disabled
            self.save_all_button = tk.Button(self.image_options_frame, text="Save", state=tk.DISABLED, command=lambda: self.save_image(self.file_path_buccal,self.file_path_maxilla, self.file_path_mandible, patient_id))
            # self.save_all_button.pack(pady=20)
            self.save_all_button.grid(row=3, column=1, padx=0, pady=10,sticky="w")
            # Mark this section as uploaded
            self.image_entries[section]["uploaded"] = True
            # Check if all images are uploaded to enable Save All button
            if all(entry["uploaded"] for entry in self.image_entries.values()):
                self.save_all_button.config(state=tk.NORMAL)
            # save_button.pack(side="left", padx=5, pady=5)


    def reupload_image(self,window, patient_id):
        window.destroy()
        self.upload_image(patient_id)
    def save_image(self,  image_path_buccal,image_path_maxilla, image_path_mandible, patient_id):
        if not image_path_buccal:
            messagebox.showerror("Error", "Image path is empty.")
            return

        # Open the image
        try:
            img = Image.open(image_path_buccal)
            img2=Image.open(image_path_maxilla)
            # img3= Image.open(image_path_lingual)
            img4=Image.open(image_path_mandible)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")
            return

        # Convert the image to bytes
        try:
            img_byte_array = BytesIO()
            img.save(img_byte_array, format='PNG')
            img_byte_array = img_byte_array.getvalue()
            
            img_byte_array2=BytesIO()
            img2.save(img_byte_array2, format='PNG')
            img_byte_array2=img_byte_array2.getvalue()
            
            # img_byte_array3=BytesIO()
            # img3.save(img_byte_array3, format='PNG')
            # img_byte_array3=img_byte_array3.getvalue()
            
            img_byte_array4=BytesIO()
            img4.save(img_byte_array4, format='PNG')
            img_byte_array4=img_byte_array4.getvalue()
            
            self.Gingivitis_detection(patient_id, img_byte_array, img_byte_array2, img_byte_array4)
        except Exception as e:  
            messagebox.showerror("Error", f"Failed to go forward image: {str(e)}")
        # self.Gingivitis_detection(patient_id, img_byte_array)
          
    

    def open_camera_capture_window(self, patient_id, section):
        
        def save_captured_image():
            if self.captured_image1 is not None:
                # Convert the image to bytes
                img_byte_array1 = io.BytesIO()
                self.captured_image1.save(img_byte_array1, format='PNG')
                img_data1 = img_byte_array1.getvalue()
                
                img_byte_array2 = io.BytesIO()
                self.captured_image2.save(img_byte_array2, format='PNG')
                img_data2 = img_byte_array2.getvalue()
                
                
                img_byte_array4 = io.BytesIO()
                self.captured_image4.save(img_byte_array4, format='PNG')
                img_data4 = img_byte_array4.getvalue()

                self.Gingivitis_detection(patient_id, img_data1, img_data2, img_data4)

        def capture_image():
            try:
                cam = cv2.VideoCapture(1)
                if not cam.isOpened():
                    raise Exception("Could not open camera.")
                
                while True:
                    ret, frame = cam.read()
                    cv2.imshow("Camera Capture", frame)
                    k = cv2.waitKey(1)
                    if k % 256 == 32:  # Space key to capture
                        break
            except cv2.error as e:
                messagebox.showerror('Error', f"OpenCV Error: {e}")
            except Exception as e:
                messagebox.showerror('Error', f"Error: {e}")
            finally:
                if 'cam' in locals() and cam.isOpened():
                    cam.release()
                    cv2.destroyAllWindows()

                if 'frame' in locals():
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    img = img.resize((300, 200), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)

                    # Clear the section frame
                    section_frame = self.image_entries[section]["frame"]
                    for widget in section_frame.winfo_children():
                        widget.destroy()

                    # Add section label above the image
                    section_label = ttk.Label(section_frame, text=f"{section.capitalize()}:", style="Custom.TLabel")
                    section_label.pack(pady=1)

                    image_label = tk.Label(section_frame, image=photo)
                    image_label.photo = photo
                    image_label.pack(padx=2 ,pady=10)

                    reupload_button = tk.Button(section_frame, text="⟲", command=capture_image)
                    reupload_button.pack(pady=5)
                    
                    self.save_all_button = tk.Button(self.image_options_frame, text="Save", state=tk.DISABLED, command=lambda: save_captured_image())
                    # self.save_all_button.pack(pady=20)
                    self.save_all_button.grid(row=3, column=1, padx=0, pady=10,sticky="w")

                    self.image_entries[section]["uploaded"] = True

                    if all(entry["uploaded"] for entry in self.image_entries.values()):
                        self.save_all_button.config(state=tk.NORMAL)
                    if(section=="buccal"):
                        self.captured_image1 = img
                    elif section=="maxilla":
                        self.captured_image2=img
                    elif section=="mandible":
                        self.captured_image4=img

        capture_image()

    
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

if __name__ == "__main__":
    app = tk.Window("Dental Clinic", "flatly", resizable=(True, True))
    DentalClinic(app)
    
    app.mainloop()
