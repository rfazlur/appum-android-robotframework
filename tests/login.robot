*** Settings ***
Resource    ../resources/keywords.robot
Suite Setup    Run Keywords
...    Start Android Emulator    headless=${emulator.headless}    boot_timeout=${emulator.bootTimeout}
...    AND    Start Appium Server
...    AND    Open Test App
Suite Teardown    Run Keywords
...    Close Test App
...    AND    Stop Appium Server
...    AND    Stop Android Emulator

*** Variables ***
${HAMBURGER_BTN}    accessibility_id=open menu
${LOG_IN_MENU}    accessibility_id=menu item log in
${USERNAME_FIELD}    accessibility_id=Username input field
${PASSWORD_FIELD}    accessibility_id=Password input field
${LOGIN_BTN}    accessibility_id=Login button
${PRODUCTS_LABEL}    xpath=//android.widget.TextView[@text="Products"]
${LOG_OUT_MENU}    accessibility_id=menu item log out
${LOGOUT_CONFIRM_BTN}    xpath=//android.widget.Button[@text="LOG OUT"]
${LOGOUT_OK_BTN}    xpath=//android.widget.Button[@text="OK"]
${ERROR_MESSAGE}    xpath=//android.widget.TextView[@text="Provided credentials do not match any user in this service."]

*** Test Cases ***
Login - Success Login With Valid Credentials
    [Documentation]    Login with valid credentials and verify success.
    Wait Until Page Contains Element    ${HAMBURGER_BTN}    timeout=15s
    Click Element    ${HAMBURGER_BTN}
    Wait Until Element Is Visible    ${LOG_IN_MENU}
    Click Element    ${LOG_IN_MENU}
    Wait Until Element Is Visible    ${USERNAME_FIELD}
    Input Text    ${USERNAME_FIELD}    bob@example.com
    Input Text    ${PASSWORD_FIELD}    10203040
    Click Element    ${LOGIN_BTN}
    Wait Until Element Is Visible    ${PRODUCTS_LABEL}
    Capture Page Screenshot    ${OUTPUT_DIR}/login-success.png

Logout - Success Logout After Login
    [Documentation]    Logout from the app and verify redirect to login screen.
    Wait Until Page Contains Element    ${HAMBURGER_BTN}    timeout=10s
    Click Element    ${HAMBURGER_BTN}
    Wait Until Element Is Visible    ${LOG_OUT_MENU}
    Click Element    ${LOG_OUT_MENU}
    Wait Until Element Is Visible    ${LOGOUT_CONFIRM_BTN}
    Click Element    ${LOGOUT_CONFIRM_BTN}
    Wait Until Element Is Visible    ${LOGOUT_OK_BTN}
    Click Element    ${LOGOUT_OK_BTN}
    Wait Until Page Contains Element    ${HAMBURGER_BTN}    timeout=10s
    Click Element    ${HAMBURGER_BTN}
    Wait Until Element Is Visible    ${LOG_IN_MENU}
    Capture Page Screenshot    ${OUTPUT_DIR}/logout-success.png
    Click Element    ${HAMBURGER_BTN}

Login - Negative Invalid Credentials
    [Documentation]    Login with invalid credentials and verify error message.
    Wait Until Page Contains Element    ${HAMBURGER_BTN}    timeout=10s
    Click Element    ${HAMBURGER_BTN}
    Wait Until Element Is Visible    ${LOG_IN_MENU}
    Click Element    ${LOG_IN_MENU}
    Wait Until Element Is Visible    ${USERNAME_FIELD}
    Input Text    ${USERNAME_FIELD}    invalid@test.com
    Input Text    ${PASSWORD_FIELD}    wrongpass
    Click Element    ${LOGIN_BTN}
    Wait Until Element Is Visible    ${ERROR_MESSAGE}
    Capture Page Screenshot    ${OUTPUT_DIR}/login-invalid-error.png
