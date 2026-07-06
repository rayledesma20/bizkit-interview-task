# Take-Home Exercise — Equipment Rental

Thanks for taking the time to do this! Instead of building something from a blank page, you'll work with a **small app that already exists** — much like you would on the job. Your task is to **find and fix some problems, and add one small feature.**

It should take around **3–4 hours**. We don't expect everything to be perfect — we mostly want to see how you read unfamiliar code, track down a problem, and make a clean fix.

---

## The app

A simple tool for renting out equipment (cameras, drills, etc.). It has:

- `app.py` — a small Python (Flask) backend with the booking logic and a JSON API
- `index.html` — a one-page frontend (plain JavaScript) for making a booking
- `bookings.json` — where bookings are stored
- `requirements.txt`

## Prerequisites

You'll need **Python 3.10 or newer** installed. Check your version with:

```bash
python3 --version    # macOS / Linux
python --version     # Windows
```

If it prints something lower than 3.10, or the command isn't found, install Python first:

- **macOS** — download the installer from [python.org/downloads](https://www.python.org/downloads/), or if you use Homebrew: `brew install python`.
- **Windows** — download the installer from [python.org/downloads](https://www.python.org/downloads/) and, on the first screen, **tick "Add python.exe to PATH"** before clicking Install. (Alternatively: `winget install Python.Python.3.12`.)

No database or other tools are needed — just Python and a web browser.

---

## Getting your own copy

Before anything else:

Click **"Use this template"** on this repository to create your own copy, then clone it to your local machine to work on it.

---

## Running the app

We recommend using a virtual environment so the dependencies stay isolated.

**On macOS / Linux:**

```bash
# from inside the project folder
python3 -m venv venv          # create a virtual environment
source venv/bin/activate      # activate it (your prompt should now show "(venv)")
pip install -r requirements.txt
python app.py
```

**On Windows (PowerShell):**

```powershell
# from inside the project folder
python -m venv venv           # create a virtual environment
venv\Scripts\Activate.ps1     # activate it (your prompt should now show "(venv)")
pip install -r requirements.txt
python app.py
```

> If PowerShell blocks the activate script with an execution-policy error, run
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once in that window, then activate again.
> If you use the classic Command Prompt (cmd.exe) instead of PowerShell, activate with `venv\Scripts\activate.bat`.

Then open **http://localhost:5000** in your browser. Have a click around first to get a feel for it. The business rules are described in a comment at the top of `app.py`.

When you're done working, you can leave the virtual environment with `deactivate`.

---

## Your tasks

### 1. The double-booking bug
A customer reported they were able to **book the same camera for dates that overlap an existing booking** — which shouldn't be allowed. Reproduce it, find the cause, and fix it. *(There's already a booking for the Canon DSLR Camera from Jan 10–15 in the data — a good place to start.)*

### 2. The PHP 0 booking bug
Some bookings are coming out with a **total of PHP 0.00**, and short rentals are being undercharged. Figure out why and fix it. *(Reminder: rentals are billed inclusively — both the start and end day count, so a same-day rental is 1 day.)*

### 3. Add a rule: no booking equipment under maintenance
Equipment can have a status of `maintenance` (the HD Projector is one). Right now it can still be booked and still shows up as available. **Add the rule that maintenance equipment cannot be booked**, and make sure it no longer appears as available. Think about all the places this rule needs to apply.

### 4. The frontend price bug
On the booking page, change the **start** date and the total updates. Change the **end** date and it... doesn't always. Find and fix it so the total stays correct.

### 5. A short write-up (`NOTES.md`)
Please include a `NOTES.md` with three quick things — keep it brief, no essays:

- **Explain one fix.** Pick any one of the bugs above and, in a few sentences, say what was actually wrong and how your fix addresses it.
- **Show the failure.** For the double-booking bug (Task 1), give one concrete example — just the dates — of a booking the *original* code **wrongly allowed**, but that your fix now correctly **blocks**. One line is fine.
- **AI use (this won't count against you).** Tell us roughly what you used AI tools for, if anything — and, importantly, **how you checked that its output was correct.** We use AI here every day; we're just looking for people who understand what they ship, not people who avoided the tools.

---

## What to send back

- The fixed code (a git repo — small commits with clear messages are appreciated).
- Your `NOTES.md` (the three short items from Task 5).

Passing the assessment leads to a follow-up call. We'll ask you to explain one of your fixes, then collaborate on adding a small feature, so approach each fix in a way you can clearly understand and discuss.

Good luck, and thank you!
