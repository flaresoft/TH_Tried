/**
 * FMOD Studio script to expand all folders in the Event Browser and list the events.
 *
 * Run this inside FMOD Studio's scripting console.
 */

// Try to obtain the Event Browser window. Different FMOD versions expose
// different helpers, so check a few possibilities before giving up.
var eventBrowser = null;

if (studio.window && typeof studio.window.find === "function") {
    eventBrowser = studio.window.find("Events");
}

// Older versions expose the window helpers on the global `ui` object.
if (!eventBrowser && typeof ui.findWindow === "function") {
    eventBrowser = ui.findWindow("Events") || ui.findWindow("Event Browser");
}

if (!eventBrowser) {
    ui.showMessageBox({
        title: "Error",
        message: "Events window is not open. Open the Events tab and run again.",
    });
    return;
}

// Locate the tree widget that backs the browser.
var tree = null;
if (typeof eventBrowser.findWidget === "function") {
    tree = eventBrowser.findWidget("tree");
} else if (typeof eventBrowser.findChild === "function") {
    // Fall back to searching for the first TreeView widget.
    tree = eventBrowser.findChild(function(w) { return w.widgetType === "TreeView"; });
}

if (!tree) {
    ui.showMessageBox({
        title: "Error",
        message: "Could not locate event tree widget. Script may require a newer FMOD version.",
    });
    return;
}

// Recursively expand every folder in the tree.
function expand(item) {
    // Expand the current item if it has children (folders/events).
    tree.expand(item);

    // Recurse into sub-items.
    for (var i = 0; i < item.numChildren; i++) {
        expand(item.getChild(i));
    }
}

expand(tree.rootItem);

// Optional: Log all event paths to the console.
var events = studio.project.model.Event.find();
for (var i = 0; i < events.length; i++) {
    var e = events[i];
    studio.log(e.path);
}
