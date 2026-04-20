🚀 CORE EVOLUTION: THE 4 MAJOR ENHANCEMENTS 
The v1.1 release introduces 4 critical functional shifts that transform the application from a basic logger into a robust data retrieval and management tool:

🛠️ 1. Advanced Entry & Data Integrity System (v0 Optimized) 
The Change: Transitioned from static data entry to a dynamic, secure recording engine.
Technical Detail: Integrated the time.strftime module to provide real-time automated timestamps. Furthermore, implemented Input Sanitization using .replace('\n', ' ') to ensure that user-generated newlines do not break the line-based ID calculation logic of the flat-file database (diary.dat).
Engineering Decision: Enforced UTF-8 Encoding to guarantee full support for Turkish characters and prevent data corruption during cross-platform execution.

📜 2. Iterative Retrieval & Data Parsing (v1 Extension) 
The Change: The system evolved from a "Write-Only" state to a fully functional "Read-and-Display" architecture.
Technical Detail: The strict "No-Loop" constraint of the initial phase was replaced by a controlled for line in f iteration in v1. Raw data strings are now Parsed using the | separator, allowing the CLI to extract and display IDs, Dates, and Content previews independently.
Engineering Decision: Designed a professional table-view output to provide a clean and readable user interface instead of dumping raw file data.

🔎 3. Intelligent Search Engine & Filtering (v1 Extension) 
The Change: Added a high-speed search layer capable of locating specific information within thousands of logs.
Technical Detail: The search command implements a string-matching algorithm across the entire database. By utilizing the .lower() method, the search engine was made completely Case-Insensitive, ensuring a flexible and user-friendly experience.
Engineering Decision: Integrated logical guardrails to prevent system crashes when no matches are found, providing clear feedback messages to the user.

🗄️ 4. Full Entry Management & Safe Deletion (v1.1 Update)
The Change: The application completed its core data lifecycle by introducing targeted reading and safe deletion capabilities.
Technical Detail: The read command utilizes an iterative search with an early break to efficiently display full-length entries. The delete command employs a safe "File Rewriting" algorithm—loading non-matching lines into memory and rewriting the database to execute deletion without data corruption.
Engineering Decision: To maintain the strict flat-file constraint without relying on external database libraries, an array-filtering and rewriting strategy was chosen over complex in-place file modifications.

Feature,v0: Restricted Core 🛠️,v1.1: Advanced Extension 🚀 
Logic Policy,"Strict ""No-Loop"" constraint.",Iterative logic enabled. 
Data Retrieval,Not implemented (Write-only).,Full Retrieval via list and read commands. 
Searchability,Static file writing.,Keyword Search engine integrated. 
Input Safety,Raw input storage.,Sanitization for DB Integrity.
Entry Management,Append-only logic.,Full control with safe deletion.

COMMAND,SYNTAX,ACTION 
INITIALIZE,python solution.py init,Sets up the hidden environment. 
WRITE,"python solution.py write ""msg""","[v0] Assigns ID, attaches Timestamp." 
LIST,python solution.py list,[v1] Iterates and prints all logs. 
SEARCH,"python solution.py search ""key""",[v1] Scans logs for specified keyword.
READ,python solution.py read <id>,[v1.1] Iteratively fetches and displays a specific entry.
DELETE,python solution.py delete <id>,[v1.1] Safely removes an entry via file rewriting.
