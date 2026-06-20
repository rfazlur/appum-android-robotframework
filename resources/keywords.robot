*** Settings ***
Library    AppiumLibrary
Library    ../resources/AppiumServerLibrary.py
Variables   variables.yaml

*** Keywords ***
Open Test App
    [Documentation]    Launch the Android app under test.
    Open Application
    ...    ${appium.server}
    ...    platformName=${device.platformName}
    ...    platformVersion=${device.platformVersion}
    ...    deviceName=${device.deviceName}
    ...    automationName=${device.automationName}
    ...    app=${app.path}
    ...    appPackage=${app.package}
    ...    appActivity=${app.activity}
    ...    appWaitActivity=${app.waitActivity}
    ...    newCommandTimeout=${appium.newCommandTimeout}
    ...    autoGrantPermissions=true
    Set Appium Timeout    ${appium.implicitWait}

Close Test App
    [Documentation]    Close the application and quit the session.
    Run Keyword And Ignore Error    Capture Page Screenshot    ${OUTPUT_DIR}/teardown-screenshot.png
    Run Keyword And Ignore Error    Close Application


