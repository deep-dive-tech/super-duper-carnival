using Toybox.Application;
using Toybox.SensorLogging;
using Toybox.ActivityRecording;
using Toybox.System;

// In windows: C:\Users\<USER>\AppData\Local\Temp\GARMIN\Activities
// In mac: $TMPDIR/Garmin/Activities

class AccelMagApp extends Application.AppBase {
    var mLogger;
    var mSession;

    function initialize() {
        AppBase.initialize();
		mLogger = new SensorLogging.SensorLogger({:enableAccelerometer => true});
		mSession = ActivityRecording.createSession({
			:name=>"Dive",
			:sport=>ActivityRecording.SPORT_GENERIC,
			:subSport=>ActivityRecording.SUB_SPORT_GENERIC ,
			:sensorLogger => mLogger
		});
	}
 
    // onStart() is called on application start up
    function onStart(state) {
        mSession.start();
    }

    // onStop() is called when your application is exiting
    function onStop(state) {
        //Sensor.unregisterSensorDataListener(method(:accel_callback));
        mSession.stop();
    }
   // Return the initial view of your application here
    function getInitialView() {
        var mainView = new AccelMagView();
        var viewDelegate = new AccelMagDelegate( mainView );
        return [mainView, viewDelegate];
    }
}