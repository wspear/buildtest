import os
import random
import string
import tempfile

import pytest
from buildtest.cli.buildspec import (
    BuildspecCache,
    buildspec_maintainers,
    buildspec_validate,
    edit_buildspec_file,
    edit_buildspec_test,
    show_buildspecs,
    show_failed_buildspecs,
    summarize_buildspec_cache,
)
from buildtest.cli.report import Report
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError
from rich.color import Color

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.cli
def test_buildspec_validate():

    buildspecs = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml"),
        os.path.join(BUILDTEST_ROOT, "tutorials", "compilers"),
    ]
    exclude_buildspecs = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "compilers", "gnu_hello_c.yml")
    ]
    tags = ["pass", "python"]
    executors = ["generic.local.sh"]

    buildspec_validate(
        buildspecs=buildspecs,
        excluded_buildspecs=exclude_buildspecs,
        tags=tags,
        executors=executors,
        configuration=configuration,
    )

    buildspec = [os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_tag.yml")]

    with pytest.raises(SystemExit):
        buildspec_validate(buildspecs=buildspec, configuration=configuration)


@pytest.mark.cli
def test_func_buildspec_find():

    # buildtest buildspec find --rebuild --terse --no-header
    cache = BuildspecCache(
        rebuild=True, configuration=configuration, terse=True, header=False
    )

    bp_dict = cache.get_cache()
    # check top-level keys in buildspec cache are present
    for key in [
        "unique_tags",
        "unique_executors",
        "buildspecs",
        "maintainers",
        "tags",
        "executor",
    ]:
        assert bp_dict[key]

    # buildtest buildspec find --rebuild
    cache = BuildspecCache(rebuild=True, configuration=configuration)
    cache.print_buildspecs()

    # buildtest buildspec find
    cache = BuildspecCache(configuration=configuration)

    # buildtest buildspec find --tags
    cache.print_tags()

    # buildtest buildspec find --buildspec
    cache.print_buildspecfiles()

    # buildtest buildspec find --paths
    cache.print_paths()

    # buildtest buildspec find --executors
    cache.print_executors()

    # buildtest buildspec find --group-by-executors
    cache.print_by_executors()

    # buildtest buildspec find --group-by-tags
    cache.print_by_tags()

    # implements buildtest buildspec find --helpfilter
    cache.print_filter_fields()

    # implements buildtest buildspec find --helpformat
    cache.print_format_fields()

    # implements buildtest buildspec find --filterfields
    cache.print_raw_filter_fields()

    # implements buildtest buildspec find --formatfields
    cache.print_raw_format_fields()

    # buildtest buildspec find --pager
    cache = BuildspecCache(configuration=configuration, pager=True)
    cache.print_tags()
    cache.print_buildspecfiles()
    cache.print_executors()
    cache.print_by_executors()
    cache.print_by_tags()
    cache.print_maintainer()
    cache.print_maintainers_by_buildspecs()
    cache.print_buildspecs()

    # buildtest buildspec find --quiet
    cache.print_buildspecs(quiet=True)

    # test buildspec cache with color 'blue'
    cache = BuildspecCache(rebuild=True, configuration=configuration, color="blue")
    cache.print_buildspecs()
    cache.print_buildspecfiles()
    cache.print_executors()
    cache.print_tags()
    cache.print_by_executors()
    cache.print_by_tags()
    cache.print_filter_fields()
    cache.print_format_fields()
    cache.print_raw_filter_fields()
    cache.print_raw_format_fields()


@pytest.mark.cli
def test_buildspec_find_terse():

    cache = BuildspecCache(
        configuration=configuration,
        terse=True,
        header=False,
        color=Color.default().name,
    )
    cache.print_buildspecs()
    cache.print_tags()
    cache.print_executors()
    cache.print_buildspecfiles()
    cache.print_by_executors()
    cache.print_by_tags()
    cache.print_maintainer()
    cache.print_maintainers_by_buildspecs()


@pytest.mark.cli
def test_buildspec_maintainers():
    buildspec_maintainers(
        configuration=configuration,
        list_maintainers=True,
        terse=True,
        header=True,
        color=Color.default().name,
    )
    buildspec_maintainers(
        configuration=configuration,
        breakdown=True,
        terse=True,
        header=True,
        color=Color.default().name,
    )
    buildspec_maintainers(configuration=configuration, name="@shahzebsiddiqui")


@pytest.mark.cli
def test_buildspec_find_invalid():
    cache = BuildspecCache(configuration=configuration)

    # testing buildtest buildspec find invalid. This will assert SystemExit exception raised by sys.exit
    try:
        cache.print_invalid_buildspecs(error=True)
    except SystemExit:
        pass

    try:
        cache.print_invalid_buildspecs(error=False)
    except SystemExit:
        pass

    try:
        cache.print_invalid_buildspecs(error=True, terse=True)
    except SystemExit:
        pass

    try:
        cache.print_invalid_buildspecs(error=False, terse=True)
    except SystemExit:
        pass

    try:
        cache.print_invalid_buildspecs(error=True, terse=True, header=True)
    except SystemExit:
        pass

    try:
        cache.print_invalid_buildspecs(error=False, terse=True, header=True)
    except SystemExit:
        pass


@pytest.mark.cli
def test_edit_test():
    edit_buildspec_test(
        test_names=["hello_world"], configuration=configuration, editor=None
    )


@pytest.mark.cli
def test_edit_file():
    edit_buildspec_file(
        buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml")],
        configuration=configuration,
        editor=None,
    )


@pytest.mark.cli
def test_buildspec_find_filter():

    # testing buildtest buildspec find --filter tags=fail
    cache = BuildspecCache(filterfields={"tags": "fail"}, configuration=configuration)
    cache.print_buildspecs()

    # testing buildtest buildspec find --filter buildspec=$BUILDTEST_ROOT/tutorials/hello_world.yml
    cache = BuildspecCache(
        filterfields={
            "buildspec": os.path.join(BUILDTEST_ROOT, "tutorials", "hello_world.yml")
        },
        configuration=configuration,
    )
    cache.print_buildspecs()

    # testing buildtest buildspec find --filter type=script,executor=generic.local.sh,tags=fail
    cache = BuildspecCache(
        filterfields={
            "type": "script",
            "executor": "generic.local.bash",
            "tags": "fail",
        },
        configuration=configuration,
    )
    cache.print_buildspecs()

    with pytest.raises(BuildTestError):
        tf = tempfile.NamedTemporaryFile()
        # testing for valid filepath for buildspec file but file doesn't exist in cache
        BuildspecCache(filterfields={"buildspec": tf.name}, configuration=configuration)

    with pytest.raises(BuildTestError):
        # create temporary file and close file which will delete the file to create invalid filepath
        tf = tempfile.NamedTemporaryFile(delete=True)
        tf.close()
        # testing on invalid file path for buildspec. This should raise an exception
        BuildspecCache(filterfields={"buildspec": tf.name}, configuration=configuration)

    with pytest.raises(BuildTestError):
        tf = tempfile.TemporaryDirectory()
        # if we specify a directory path for buildspec filter this will raise an exception.
        BuildspecCache(filterfields={"buildspec": tf.name}, configuration=configuration)

    # testing buildtest buildspec find --filter key1=val1,key2=val2
    with pytest.raises(BuildTestError):
        cache = BuildspecCache(
            filterfields={"key1": "val1", "key2": "val2"}, configuration=configuration
        )
        cache.print_buildspecs()


@pytest.mark.cli
def test_buildspec_find_format():

    # testing buildtest buildspec find --format name,type,tags,executor,description,buildspec
    cache = BuildspecCache(
        formatfields="name,type,tags,executor,description,buildspec",
        configuration=configuration,
    )
    cache.print_buildspecs()

    # Any invalid format fields will raise an exception of type BuildTestError
    with pytest.raises(BuildTestError):

        # testing buildtest buildspec find --format field1
        cache = BuildspecCache(formatfields="field1", configuration=configuration)
        cache.print_buildspecs()


@pytest.mark.cli
def test_buildspec_find_roots():

    root_buildspecs = [
        os.path.join(BUILDTEST_ROOT, "tests", "buildsystem"),
        os.path.join(BUILDTEST_ROOT, "tutorials"),
    ]
    # testing buildtest buildspec find --root $BUILDTEST_ROOT/tests/buildsystem --root $BUILDTEST_ROOT/tutorials
    BuildspecCache(roots=root_buildspecs, configuration=configuration)

    # running buildtest buildspec find --root $BUILDTEST_ROOT/README.rst --root $BUILDTEST_ROOT/environment.yml
    BuildspecCache(
        roots=[
            os.path.join(BUILDTEST_ROOT, "README.rst"),
            os.path.join(BUILDTEST_ROOT, "tutorials", "environment.yml"),
        ],
        configuration=configuration,
    )


@pytest.mark.cli
def test_buildspec_summary():
    # test buildtest buildspec summary
    summarize_buildspec_cache(
        configuration=configuration, pager=False, color=Color.default().name
    )
    summarize_buildspec_cache(configuration=configuration, pager=True)


@pytest.mark.cli
def test_buildspec_show():
    cache = BuildspecCache(configuration=configuration)

    test_name = cache.get_random_tests(num_items=1)

    # run buildtest buildspec show <test>
    show_buildspecs(test_name, configuration)

    # run buildtest buildspec <test> show --theme monokai
    show_buildspecs(test_name, configuration, theme="monokai")

    # testing invalid buildspec name, it should not raise exception
    random_testname = "".join(random.choices(string.ascii_letters, k=10))
    show_buildspecs(test_names=[random_testname], configuration=configuration)


@pytest.mark.cli
def test_buildspec_show_fail():

    # Query some random test name that doesn't exist

    random_testname = "".join(random.choices(string.ascii_letters, k=10))
    show_failed_buildspecs(configuration=configuration, test_names=[random_testname])

    # Query a test that is NOT in state=FAIL

    results = Report()
    pass_test = random.sample(results.get_test_by_state(state="PASS"), 1)
    show_failed_buildspecs(configuration=configuration, test_names=[pass_test])

    report = Report()
    # get a random failed test from report file to be used for showing content of buildspec file
    fail_tests = random.sample(report.get_test_by_state(state="FAIL"), 1)
    # running buildtest buildspec show-fail <test> --theme monokai
    show_failed_buildspecs(
        configuration=configuration, test_names=fail_tests, theme="monokai"
    )
