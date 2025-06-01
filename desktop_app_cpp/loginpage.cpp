#include "loginpage.h"

#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QCheckBox>
#include <QVBoxLayout>
#include <QDebug> // For status messages and login attempts

#include "Printago/Agents/IAuthService.h" // Needed for m_authService->login() call

LoginPage::LoginPage(IAuthService* authService, QWidget *parent)
    : QWidget(parent), m_authService(authService)
{
    Q_ASSERT(m_authService != nullptr); // Ensure authService is provided at construction

    QVBoxLayout *layout = new QVBoxLayout(this);

    QLabel *titleLabel = new QLabel("Connect your Bambu Lab Account", this);
    titleLabel->setAlignment(Qt::AlignCenter);

    emailInput = new QLineEdit(this);
    emailInput->setPlaceholderText("Enter your Bambu Lab email");

    passwordInput = new QLineEdit(this);
    passwordInput->setPlaceholderText("Password");
    passwordInput->setEchoMode(QLineEdit::Password);

    rememberMeCheckbox = new QCheckBox("Remember Me", this);

    loginButton = new QPushButton("Login", this);
    connect(loginButton, &QPushButton::clicked, this, &LoginPage::onLoginButtonClicked);

    statusLabel = new QLabel("", this); // Initially empty
    statusLabel->setAlignment(Qt::AlignCenter);

    layout->addWidget(titleLabel);
    layout->addWidget(emailInput);
    layout->addWidget(passwordInput);
    layout->addWidget(rememberMeCheckbox);
    layout->addWidget(loginButton);
    layout->addWidget(statusLabel);

    layout->setSpacing(15);
    emailInput->setMaximumWidth(300);
    passwordInput->setMaximumWidth(300);
    rememberMeCheckbox->setMaximumWidth(300);
    loginButton->setMaximumWidth(150);

    setLayout(layout);
}

void LoginPage::onLoginButtonClicked()
{
    if (!m_authService) {
        statusLabel->setText("Error: Authentication service not available.");
        qWarning() << "LoginPage: m_authService is null!";
        return;
    }

    QString email = emailInput->text();
    QString password = passwordInput->text();

    if (email.isEmpty() || password.isEmpty()) {
        statusLabel->setText("Email and password cannot be empty.");
        return;
    }

    statusLabel->setText("Logging in...");
    loginButton->setEnabled(false); // Disable button during login attempt

    m_authService->login(email, password, [this, email](bool success, const QString& message) {
        // This lambda is called when the async login operation completes
        statusLabel->setText(message);
        loginButton->setEnabled(true); // Re-enable button regardless of outcome

        if (success) {
            qDebug() << "Login successful for:" << email;
            // passwordInput->clear(); // Optionally clear password
            // Depending on app flow, could emit a signal: e.g., emit loginSuccessful();
        } else {
            qDebug() << "Login failed for:" << email << "Error:" << message;
            passwordInput->clear(); // Clear password on failure to allow re-try
            passwordInput->setFocus();
        }
    });
}
