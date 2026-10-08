import streamlit as st
import json
import hashlib
import time
import pandas as pd
from student import Student
from Database import Database
from Chatbot import Chatbot

# ---------------------------------------------------------
# Page Configuration & Advanced Theme Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nexus Premium | Student Management",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dynamic UI/UX & Animations
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Keyframe Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(140, 77, 255, 0.2); }
        50% { box-shadow: 0 0 25px rgba(140, 77, 255, 0.6); }
        100% { box-shadow: 0 0 10px rgba(140, 77, 255, 0.2); }
    }

    @keyframes floatHero {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }

    /* Main Container Animation */
    .element-container, .stMarkdown, div[data-testid="stMetricValue"] {
        animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Glassmorphism Card Containers */
    .nexus-card {
        background: rgba(22, 27, 34, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .nexus-card:hover {
        transform: translateY(-4px);
        border-color: rgba(140, 77, 255, 0.4);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
    }

    /* Animated Hero Header */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #8c4dff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        animation: floatHero 6s ease-in-out infinite;
    }

    /* Animated Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 16px 20px;
        transition: all 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #8c4dff;
        transform: scale(1.02);
    }

    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #8c4dff !important;
    }

    /* Custom Chat Bubbles */
    .chat-bubble-user {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        color: #f3f4f6;
        padding: 14px 20px;
        border-radius: 18px 18px 4px 18px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        animation: fadeIn 0.4s ease;
    }

    .chat-bubble-bot {
        background: linear-gradient(135deg, rgba(140, 77, 255, 0.15) 0%, rgba(22, 27, 34, 0.8) 100%);
        color: #f3f4f6;
        padding: 14px 20px;
        border-radius: 18px 18px 18px 4px;
        margin-bottom: 12px;
        border: 1px solid rgba(140, 77, 255, 0.3);
        animation: fadeIn 0.4s ease;
    }

    /* Custom Glowing Button Styles */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease-in-out !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(140, 77, 255, 0.35) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Functions for Authentication
# ---------------------------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_credentials():
    with open('credentials.json', 'r') as f:
        return json.load(f)

def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

def save_users(users_data):
    with open('users.json', 'w') as f:
        json.dump(users_data, f, indent=4)

# ---------------------------------------------------------
# Initialize Core Instances & Session State
# ---------------------------------------------------------
db = Database()
bot = Chatbot(db)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# ---------------------------------------------------------
# Sidebar: Brand & Authentication
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<h1 style="font-size: 2.2rem; font-weight: 800; color: #8c4dff;">⚡ NEXUS</h1>', unsafe_allow_html=True)
    st.caption("Next-Gen Student Database Intelligence")
    st.divider()

    if not st.session_state['authenticated']:
        auth_mode = st.segmented_control(
            "Access Mode",
            ["Login", "Register"],
            default="Login"
        )
        
        st.write("")
        username_input = st.text_input("Username", placeholder="e.g. alex_dev")
        password_input = st.text_input("Password", type="password", placeholder="••••••••")

        if auth_mode == "Login":
            if st.button("🚀 Sign In", use_container_width=True, type="primary"):
                hashed_input = hash_password(password_input)
                
                # Check Admin Credentials
                admin_creds = load_credentials().get("admin", {})
                if username_input == admin_creds.get("username") and hashed_input == admin_creds.get("password"):
                    st.session_state['authenticated'] = True
                    st.session_state['user_role'] = 'admin'
                    st.session_state['username'] = username_input
                    st.toast("Welcome back, Administrator!", icon="👑")
                    time.sleep(0.4)
                    st.rerun()
                
                # Check Normal User Credentials
                else:
                    users_list = load_users().get("users", [])
                    user_found = next((u for u in users_list if u['username'] == username_input and u['password'] == hashed_input), None)
                    if user_found:
                        st.session_state['authenticated'] = True
                        st.session_state['user_role'] = 'user'
                        st.session_state['username'] = username_input
                        st.toast(f"Welcome back, {username_input}!", icon="👋")
                        time.sleep(0.4)
                        st.rerun()
                    else:
                        st.error("Authentication failed. Invalid credentials.")

        elif auth_mode == "Register":
            if st.button("✨ Create Account", use_container_width=True, type="primary"):
                if username_input and password_input:
                    users_data = load_users()
                    existing_user = next((u for u in users_data['users'] if u['username'] == username_input), None)
                    
                    if existing_user or username_input == "admin":
                        st.error("Username is taken. Choose another.")
                    else:
                        users_data['users'].append({
                            "username": username_input,
                            "password": hash_password(password_input)
                        })
                        save_users(users_data)
                        st.success("Account created! Switch to Login.")
                else:
                    st.warning("Please provide both username and password.")

    else:
        st.markdown(f"""
        <div class="nexus-card">
            <small style="color: #8b949e; letter-spacing: 1px;">ACTIVE SESSION</small><br>
            <strong style="font-size: 1.2rem; color: #ffffff;">{st.session_state['username']}</strong><br><br>
            <span style="background: rgba(140, 77, 255, 0.2); color: #8c4dff; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; border: 1px solid rgba(140, 77, 255, 0.4);">
                ● {st.session_state['user_role'].upper()}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔒 Sign Out", use_container_width=True):
            st.session_state['authenticated'] = False
            st.session_state['user_role'] = None
            st.session_state['username'] = None
            st.session_state['chat_history'] = []
            st.rerun()

# ---------------------------------------------------------
# Main App Layout
# ---------------------------------------------------------
if not st.session_state['authenticated']:
    # Animated Landing Screen
    st.markdown("""
    <div style="text-align: center; padding: 100px 20px 40px 20px;">
        <h1 class="hero-title">🎓 Nexus Management System</h1>
        <p style="font-size: 1.25rem; color: #8b949e; max-width: 650px; margin: 20px auto 40px auto; line-height: 1.6;">
            Empowering modern data management with an elegant architecture. High performance, role-based access, and conversational query processing built-in.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div class="nexus-card">
            <h3 style="color: #8c4dff; margin-bottom: 8px;">⚡ Fast Operations</h3>
            <p style="color: #8b949e; font-size: 0.95rem;">Seamless CRUD operations backed by MySQL connectivity and parameterized queries.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div class="nexus-card">
            <h3 style="color: #8c4dff; margin-bottom: 8px;">🔒 Role Auth</h3>
            <p style="color: #8b949e; font-size: 0.95rem;">Hashed SHA-256 credentials ensuring granular access control for users and admins.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div class="nexus-card">
            <h3 style="color: #8c4dff; margin-bottom: 8px;">🤖 AI Querying</h3>
            <p style="color: #8b949e; font-size: 0.95rem;">Interact directly with records through a natural language chatbot processor.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Top Metrics Banner
    raw_records = db.fetch_all_students()
    total_students = len(raw_records) if raw_records else 0
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Total Enrolled", total_students, delta="Live Sync")
    with col_m2:
        grades = [r[3] for r in raw_records] if raw_records else []
        top_grade = max(set(grades), key=grades.count) if grades else "N/A"
        st.metric("Top Grade Tier", top_grade)
    with col_m3:
        ages = [r[2] for r in raw_records] if raw_records else [0]
        avg_age = round(sum(ages) / len(ages), 1) if raw_records else 0
        st.metric("Average Student Age", f"{avg_age} yrs")
    with col_m4:
        st.metric("System Health", "Optimal", delta="MySQL Active", delta_color="normal")

    st.write("")

    # Role-Based Tabs
    if st.session_state['user_role'] == 'admin':
        tab_view, tab_manage, tab_bot = st.tabs(["📊 Analytics & Data", "🛠️ Record Operations", "🤖 AI Assistant"])
    else:
        tab_view, tab_bot = st.tabs(["📊 View Records", "🤖 AI Assistant"])
        tab_manage = None

    # TAB 1: VIEW & ANALYTICS
    with tab_view:
        st.markdown("### 📋 Student Directory")
        if raw_records:
            df = pd.DataFrame(raw_records, columns=["ID", "Name", "Age", "Grade"])
            
            search_col, grade_col = st.columns([3, 1])
            with search_col:
                search_term = st.text_input("🔍 Search by name...", placeholder="Type student name...", label_visibility="collapsed")
            with grade_col:
                selected_grade = st.selectbox("Filter Grade", ["All Grades"] + sorted(list(set(df['Grade']))), label_visibility="collapsed")

            # Apply Dynamic Filters
            filtered_df = df.copy()
            if search_term:
                filtered_df = filtered_df[filtered_df['Name'].str.contains(search_term, case=False)]
            if selected_grade != "All Grades":
                filtered_df = filtered_df[filtered_df['Grade'] == selected_grade]

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn("Student ID", format="%d"),
                    "Age": st.column_config.NumberColumn("Age", format="%d yrs"),
                    "Grade": st.column_config.TextColumn("Academic Grade")
                }
            )
        else:
            st.info("No records currently available in MySQL.")

    # TAB 2: ADMIN OPERATIONS
    if tab_manage:
        with tab_manage:
            st.markdown("### 🛠️ Database Control Center")
            
            op_col1, op_col2 = st.columns([1, 2])
            
            with op_col1:
                st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
                action = st.radio(
                    "Select Action",
                    ["➕ Register Student", "✏️ Update Student", "🗑️ Delete Student", "📂 Bulk CSV Upload"]
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with op_col2:
                if action == "➕ Register Student":
                    st.markdown("##### Add New Record")
                    with st.form("add_student_form", clear_on_submit=True):
                        new_name = st.text_input("Full Name")
                        col_a1, col_a2 = st.columns(2)
                        with col_a1:
                            new_age = st.number_input("Age", min_value=1, max_value=100, value=20)
                        with col_a2:
                            new_grade = st.text_input("Grade (e.g. A, B+)")
                        
                        if st.form_submit_button("Save Student", type="primary"):
                            if new_name and new_grade:
                                db.insert_student(Student(name=new_name, age=new_age, grade=new_grade))
                                st.toast(f"Successfully added **{new_name}**!", icon="✅")
                                time.sleep(0.4)
                                st.rerun()
                            else:
                                st.warning("Please fill out all required fields.")

                elif action == "✏️ Update Student":
                    st.markdown("##### Modify Existing Record")
                    target_id = st.number_input("Enter Target Student ID", min_value=1, step=1)
                    
                    existing = db.fetch_students_by_id(target_id)
                    if existing:
                        st.caption(f"Current Record: Name: **{existing[1]}** | Age: **{existing[2]}** | Grade: **{existing[3]}**")
                    else:
                        st.caption("⚠️ No matching record found for this ID.")
                    
                    with st.form("update_student_form"):
                        up_name = st.text_input("New Name (Leave empty to keep existing)")
                        col_u1, col_u2 = st.columns(2)
                        with col_u1:
                            up_age = st.number_input("New Age (0 to keep existing)", min_value=0, max_value=100, value=0)
                        with col_u2:
                            up_grade = st.text_input("New Grade (Leave empty to keep existing)")
                        
                        if st.form_submit_button("Apply Updates", type="primary"):
                            # Use existing values if inputs are left blank
                            final_name = up_name if up_name else (existing[1] if existing else None)
                            final_age = up_age if up_age > 0 else (existing[2] if existing else None)
                            final_grade = up_grade if up_grade else (existing[3] if existing else None)

                            student_obj = Student(
                                student_id=target_id,
                                name=final_name,
                                age=final_age,
                                grade=final_grade
                            )
                            
                            success, message = db.update_student(student_obj)
                            if success:
                                st.toast(message, icon="✨")
                                time.sleep(0.4)
                                st.rerun()
                            else:
                                st.error(message)

                # NEW UPDATED CODE
                elif action == "🗑️ Delete Student":
                    st.markdown("##### Remove Student Entry")
                    del_id = st.number_input("Student ID to Delete", min_value=1, step=1)
                    
                    st.warning("⚠️ Action cannot be undone.")
                    if st.button("Confirm Deletion", type="primary"):
                        success, message = db.delete_student(del_id)
                        if success:
                            st.toast(message, icon="🗑️")
                            time.sleep(0.4)
                            st.rerun()
                        else:
                            st.error(message)

                elif action == "📂 Bulk CSV Upload":
                    st.markdown("##### Batch Import CSV")
                    st.caption("CSV header must contain: `name`, `age`, `grade`")
                    file_buffer = st.file_uploader("Select File", type=["csv"])
                    
                    if file_buffer and st.button("Execute Import Batch", type="primary"):
                        db.bulk_insert_csv(file_buffer)
                        st.toast("Batch import finished!", icon="🎉")
                        time.sleep(0.4)
                        st.rerun()

    # TAB 3: CHATBOT INTERFACE
    with tab_bot:
        st.markdown("### 🤖 Assistant Interface")
        st.caption("Ask natural language queries regarding the student records.")
        
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state['chat_history']:
                if message["role"] == "user":
                    st.markdown(f'<div class="chat-bubble-user">👤 <b>You:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble-bot">🤖 <b>Nexus Assistant:</b><br>{message["content"]}</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("Prompt", placeholder="Type: 'Show all students', 'How many students are there?', or 'Find student 2'", label_visibility="collapsed")
            submit_chat = st.form_submit_button("Send Query 🚀", type="primary")

            if submit_chat and user_input:
                st.session_state['chat_history'].append({"role": "user", "content": user_input})
                bot_reply = bot.process_query(user_input)
                st.session_state['chat_history'].append({"role": "assistant", "content": bot_reply})
                st.rerun()