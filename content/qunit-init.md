Title: QUnit: Module initialization
Date: 2015-01-20
Category: blogpost
Tags: JavaScript, QUnit, unit testing, functional
Slug: qunit-module-init
Author: Will Acton
Summary: 

Fun fact: I started a new job back in September doing front end development! Thus, the lack of posts recently. However, today I have something neat that I thought was worth sharing.

A large part of my new job has been learning about and writing unit tests with our projects. The framework we decided to use is [QUnit](http://qunitjs.com), a testing framework developed by the same team that maintains JQuery. It has a fairly simple API, and easy integration with Grunt and other tools we use in our workflow.

The API contains your standard assertions: equals, notEquals, ok (for generic truth-y checking), and more specific assertions like deepEquals, which allows us to compare JavaScript objects by their key/value pairs.

QUnit also gives us a way to separate our tests into 'modules'. This can be a good way to organize our tests, as well as set specific functions to be run before each test (defined in our QUnit module). Such as:

    :::javascript
    QUnit.module('View module', {
        beforEach: function (assert) {
            // do specific setup instructions before each test
        },
        afterEach: function (assert) {
            // do specific teardown instructions after each test
        }
    });


However, there are some functions that we want to run before our tests that may be resource (CPU, memory, network, etc.) intensive. Usually we only want to run these once, at most, and then cache the data for later. We could do this in the global scope, but depending on the nature of the tests this could introduce side effects into our test code.

Enter: Once(), a function inspired by the lodash/underscore library. It's a very nice function; it looks like this:

    :::javascript
    var Once = function (func) {
        var isFirst = true,
            retVal = null;

        return function (args) { // args is an array of arguments to pass to the function
            if (isFirst) { // if first time running the function
                retVal = func.apply(this, args); // run the function with the given argument list, cache the result
                isFirst = false; // don't run it again
                func = null; // clear the function from memory (to be GCed)
                return retVal; // return the value
            }
            else { // if we've already run the function
                return retVal; // return the cached value
            }
        }
    }

'Once()' returns a new function that, as the name suggests, will only actually run once. After the first time, the result is cached and returned for each subsequent call.

A useful example would be an AJAX request. Maybe we want to request some data (that we can easily swap out depending on changing requirements) and use that in our tests. The request could look something like this:

    :::javascript
    var request = function (assert) {
        var done = assert.async(); // QUnit's assert.async() function tells the framework to pause all tests until done() is called.

        var promise = $.get('data/example.json');
        promise.always(function () {
            done();
        });

        return promise;
    }

However, if we ran this before every test, it would send the request over the network each time a test was run; if the data is sizeable, it could seriously slow down our build time. Instead, let's use Once() to create a new function that will cache the result the first time it's run, and then throw it in our module definition:

    :::javascript
    var moduleInit = Once(request);

    QUnit.module('View module', {
        beforeEach: function (assert) {
            var $r = moduleInit([assert]); // func.apply() requires us to pass our arguments in as an array

            $r.done(function (data) {
                // do something with the data
            });
        },
        afterEach: function (assert) {
            // do specific teardown instructions after each test
        }
    });

Now, the request will only be run the first time, and the whole module will be run once the asynchronous request returns the data needed. In a module with lots of tests, even for a small amount of data this can shave off a large percentage of run time.