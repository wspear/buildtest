def buildtest_help():
    """Entry point for ``buildtest help`` which display a summary of how to use buildtest commands"""

    print(
        """
    Building Buildspecs
    --------------------
    
    Build a single buildspec file
    $ buildtest build -b <file> 
    
    Search all buildspecs recursively in a given directory for all '.yml' files and build all buildspecs
    $ buildtest build -b <dir>
    
    Build buildspecs by file and directory
    $ buildtest build -b <file> -b <dir>
    
    Exclude files when building buildspecs
    $ buildtest build -b <file> -b <dir> -x <file> -x <dir>
    
    Building buildspecs by tag
    $ buildtest build -t <tagname1> -t <tagname2>
    
    Building buildspecs by executor
    $ buildtest build -e <executor1> -e <executor2>
    
    building buildspecs with file, directory, tags, and executors
    $ buildtest build -b <file> -b <dir> -t <tagname1> -e <executor1>
    
    Filter tests by tagname for all buildspecs discovered
    $ buildtest build -b <file> -t <tagname1> -ft <filter-tagname1> -ft <filter-tagname2>
    
    Specify alternate buildtest configuration file when building test. 
    $ buildtest -c <config> build -b <file>
    
    Specify alternate location of test directory (/tmp)
    $ buildtest build -b <file> --testdir /tmp
    
    Set max-pend-time to 30s which overrides 'max_pend_time' field in configuration file.  buildtest will cancel job
    job if its pending in queue beyond max-pend-time value
    $ buildtest build -b <file> --max-pend-time 30
    
    Set pollinterval to 60s which overrides 'pollinterval' field in configuration file. buildtest will poll jobs based on 'pollinterval' value.
    $ buildtest build -b <file> --poll-interval 60
    
    
    View report 
    ------------
    
    Display all tests results
    $ buildtest report
    
    Filter test results by returncode=0
    $ buildtest report --filter returncode=0
    
    Filter test by multiple filter fields. In this example, buildtest will report all tests that 'PASS' for tagname 'python'
    $ buildtest report --filter state=PASS,tags=python
    
    Format report table by --format fields, in this example we only report columns 'name', 'state', 'buildspec'
    $ buildtest report --format name,state,buildspec
    
    List all filter fields
    $ buildtest report --helpfilter
    
    List all format fields
    $ buildtest report --helpformat
    
    Retrieve oldest record for all tests based on timestamp
    $ buildtest report --oldest
    
    Retrieve latest record for all tests based on timestamp
    $ buildtest report --latest
    
    Specify alternate report file to display test results
    $ buildtest report -r <report-file>
    
    
    Inspect Tests
    -------------
    
    Display record of all runs for test name 'hello'. 
    $ buildtest inspect name hello
    
    Display record of test name 'foo' and 'bar'
    $ buildtest inspect name foo bar
    
    Display all test names and ids
    $ buildtest inspect list
    
    Display record of test by unique identifer
    $ buildtest inspect id <ID>
    
    Finding Buildspecs
    ----------------------
    
    Discover and validate all buildspecs and load all validated buildspecs in cache. Finally buildtest will report all tests for all validated buildspecs
    $ buildtest buildspec find  
    
    Rebuild cache
    $ buildtest buildspec find --rebuild
    
    List all available buildspecs from cache
    $ buildtest buildspec find --buildspec
    
    List all unique tags from cache
    $ buildtest buildspec find --tags
    
    List all unique executors from cache
    $ buildtest buildspec find --executors 
    
    List all maintainers from cache
    $ buildtest buildspec find --maintainers
    
    Show breakdown of all buildspecs by maintainer names.
    $ buildtest buildspec find --maintainers-by-buildspecs
    
    Validate buildspecs
    ---------------------
    
    Validate buildspecs by file and directory
    $ buildtest buildspec validate -b <file> -b <dir>
    
    Validate buildspecs by tagname 'python' and 'mac' 
    $ buildtest buildspec validate -t python -t mac
    
    Validate buildspecs by executor name 
    $ buildtest buildspec validate -e <executor>
     
    Build History
    ---------------
    
    The 'buildtest history' command can report history of all builds when you run 'buildtest build' command
    along with log files.
    
    To display a list of all builds 
    $ buildtest history list
    
    Query information for a given build by unique identifier.
    $ buildtest history query <ID>
    
    Get logfile for given build 
    $ buildtest history query <ID> --log
    
    Buildtest Configuration 
    ------------------------
    
    View content of configuration file
    $ buildtest config view
    
    Validate configuration file with JSON schema
    $ buildtest config validate
    
    List all executors from configuration file
    $ buildtest config executors
    
    List all available system entries in configuration file
    $ buildtest config systems
    
    Specify alternate configuration file 
    $ buildtest -c <config> config validate
    
    Upload Tests to CDASH
    ---------------------
    
    Upload all tests to cdash with build name 'DEMO'
    $ buildtest cdash upload DEMO
    
    Upload all tests from report file /tmp/result.json with build name 'DAILY_CHECK'
    $ buildtest cdash upload 'DAILY_CHECK' --report /tmp/result.json
    
    Upload tests to CDASH with site named called 'laptop' 
    $ buildtest cdash upload --site laptop DEMO
    
    Open CDASH project in web-browser
    $ buildtest cdash view
    
    Open CDASH project with url name
    $ buildtest cdash view --url https://my.cdash.org/index.php?project=buildtest
    """
    )
