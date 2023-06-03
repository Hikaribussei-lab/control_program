#define FUNC_NAME 64
enum ImportedProcState
{
	ipsUnknown = 0,  // No attempts to load the Proc have been made yet
	ipsMissing,      // GetProcAddress failed to find the exported function
	ipsAvailable,    // the Proc is Ready & Available for use
	ips_MAX
};

// the structure ImportedFunc describes the data for access of the dll function 
// as long as the current status of the connection 
typedef struct ImportedFunc
{
  char Name[FUNC_NAME]; // the name of the function
  ImportedProcState Status; 
  void * ptrToFunc;
} ImportedFunc;

class DllLoader
{
  private:
    HMODULE  m_module;          // Handle to the DLL
	  DWORD    m_dwLoadLibError;  // If there was an error from LoadLibrary
	  BOOL     m_bManaged;        // FreeLibrary in the destructor?
	  LPTSTR   m_pszModule;       // The name of the module, handy for first-use loading
  protected:
	  
	  BOOL    LoadLibrary(LPCTSTR pszLibrary); // Loads the dll.  
	  BOOL    LoadLibraryName(LPCTSTR pszLibrary);    
	  FARPROC GetProcAddress(LPCSTR pszFunctionName, ImportedProcState& ips); // Loads the function pointer from the DLL
	
	
  public:
	  DllLoader();
    ~DllLoader();
    DWORD   GetLoadError()  ; // If LoadLibrary failed, returns the error code
	  BOOL    IsLoaded();      
	  LPCTSTR GetModuleName() ; // return the name of the module loaded

};

