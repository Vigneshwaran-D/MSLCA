# 🔐 User ID Persistence - How to Access Your Data

**Date:** November 18, 2025  
**Issue Fixed:** User ID no longer auto-generates randomly  
**Your User ID:** `user-d1850539`

---

## ✅ What Was Fixed

### **BEFORE (Problem):**
- User ID was being auto-generated randomly if left blank
- You couldn't access your previous data
- Each session created a new random User ID
- No way to return to your memories

### **AFTER (Fixed):**
- ✅ You manually enter your User ID
- ✅ Same User ID = access to YOUR data
- ✅ Persistent across sessions
- ✅ No more random generation
- ✅ Works for long-term and short-term memory

---

## 🚀 How to Use Your User ID

### **Step 1: Enter Your User ID**

In the Streamlit sidebar, you'll see:

```
User ID
[user-d1850539          ]  ← Enter your User ID here
```

**Your User ID:** `user-d1850539`

### **Step 2: Use It Consistently**

**Important:** Always use the SAME User ID to access your data!

✅ **Correct:**
- Session 1: Enter `user-d1850539`
- Session 2: Enter `user-d1850539` ← Same data!
- Session 3: Enter `user-d1850539` ← Same data!

❌ **Wrong:**
- Session 1: Enter `user-d1850539`
- Session 2: Leave blank or use different ID ← Different data!

---

## 📊 How User ID Works

### **Data Isolation**

Each User ID has its own isolated data:

```
Organization: 1234
├── User: user-d1850539
│   ├── 40 Episodic Events
│   ├── 25 Chat Messages
│   └── All YOUR memories
│
├── User: user-12345678  
│   └── Different user's data
│
└── User: user-abcdef01
    └── Another user's data
```

### **Current Data (Your Account)**

| Item | Count | User ID |
|------|-------|---------|
| Episodic Events | 40 | user-d1850539 |
| Chat Messages | 25 | user-d1850539 |
| Organization | 1234 | (shared) |

---

## 🎯 Common Scenarios

### **Scenario 1: First Time User**

1. Launch Streamlit: `streamlit run streamlit_app.py`
2. In sidebar, enter:
   - Organization ID: `1234`
   - User ID: `user-d1850539` ← Your chosen ID
3. Click "Connect to Database"
4. Your data will be saved under this User ID

### **Scenario 2: Returning User**

1. Launch Streamlit: `streamlit run streamlit_app.py`
2. In sidebar, enter THE SAME IDs:
   - Organization ID: `1234`
   - User ID: `user-d1850539` ← SAME as before!
3. You'll see all your previous data!

### **Scenario 3: Multiple Users**

If you want separate accounts:

**Account 1:**
- User ID: `user-d1850539`
- Has: 40 events, 25 chats

**Account 2:**
- User ID: `user-12345678`
- Has: Fresh start, no data yet

### **Scenario 4: Forgot Your User ID**

If you forgot your User ID, you can:

1. Check the database directly:
```sql
SELECT DISTINCT user_id FROM episodic_memory WHERE organization_id = '1234';
```

2. Or check your previous documentation/notes

3. Or generate test data knows it's `user-d1850539` for your test account

---

## 💾 What Gets Saved Per User ID

### **Episodic Memories**
- All events you've created
- Access counts
- Temporal scores
- Importance ratings

### **Chat Messages**
- All conversations
- Chat sessions
- Message history

### **Semantic Memories**
- Facts and concepts
- Knowledge entries

### **Procedural Memories**
- Skills and procedures

### **Resource Memories**
- Links and references

### **Knowledge Vault**
- Important knowledge items

**All isolated by User ID!**

---

## 🔒 Security & Privacy

### **Data Isolation**

- Each User ID sees ONLY their own data
- Organization admin could see all users in their org
- No cross-user data leakage

### **User ID Format**

User IDs should follow this pattern:
```
user-XXXXXXXX

Where XXXXXXXX is 8 hexadecimal characters
Examples:
- user-d1850539 ✓
- user-12345678 ✓
- user-abcdef01 ✓
```

---

## 🧪 Testing with Your User ID

### **View Your Data in Database View Tab:**

1. Go to **"🗄️ Database View"** tab
2. Select memory type (e.g., "Episodic Events")
3. See YOUR 40 events (for user-d1850539)

### **Generate More Data for Your Account:**

```bash
cd C:\Projects\MIRIX
python temp/scripts/quick_generate_data.py
```

This adds data specifically for:
- Organization: `1234`
- User: `user-d1850539`

---

## ⚠️ Important Notes

### **1. User ID is Case-Sensitive**

```
✓ user-d1850539  ← Correct
✗ USER-D1850539  ← Different user!
✗ User-D1850539  ← Different user!
```

### **2. Don't Leave User ID Blank**

If you leave User ID blank:
- ❌ Chat messages won't be saved
- ❌ You'll get warnings
- ❌ No data persistence

### **3. Write Down Your User ID**

**Your User ID:** `user-d1850539`

Save this somewhere! You'll need it every time you launch Streamlit.

### **4. Organization ID Also Required**

Both IDs are needed:
- **Organization ID:** `1234` ← Shared across users in org
- **User ID:** `user-d1850539` ← Your personal account

---

## 📝 Quick Reference Card

```
┌─────────────────────────────────────────┐
│   MIRIX USER ID REFERENCE CARD          │
├─────────────────────────────────────────┤
│                                         │
│  Organization ID:  1234                 │
│  User ID:          user-d1850539        │
│                                         │
│  Data Counts:                           │
│    - Episodic Events:   40              │
│    - Chat Messages:     25              │
│                                         │
│  To Access:                             │
│    1. Launch Streamlit                  │
│    2. Enter BOTH IDs in sidebar         │
│    3. Click "Connect to Database"       │
│    4. View your data!                   │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎉 Summary

### **What You Need to Remember:**

1. ✅ **Your User ID:** `user-d1850539`
2. ✅ **Your Org ID:** `1234`
3. ✅ **Always use the same User ID** to access your data
4. ✅ **Don't leave it blank** or it won't save
5. ✅ **Write it down** so you don't forget

### **What Changed:**

- ❌ **Before:** Random auto-generation (problem)
- ✅ **After:** Manual entry, persistent (fixed!)

---

## 🚀 Next Steps

1. **Restart Streamlit** to load the fixed code
2. **Enter your User ID** in the sidebar: `user-d1850539`
3. **Enter your Org ID** in the sidebar: `1234`
4. **Click "Connect to Database"**
5. **Go to Database View tab** and see YOUR 40 episodic events!

---

**Your data is now persistent and accessible with your User ID!** 🎉

No more random generation - you're in control! 🔐

