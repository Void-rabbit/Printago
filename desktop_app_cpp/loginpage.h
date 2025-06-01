#ifndef LOGINPAGE_H
#define LOGINPAGE_H

#include <QWidget>

// Forward declarations for Qt classes to reduce include overhead in header
class QLabel;
class QLineEdit;
class QPushButton;
class QCheckBox;
class QVBoxLayout;
class IAuthService; // Forward declaration

class LoginPage : public QWidget
{
    Q_OBJECT

public:
    explicit LoginPage(IAuthService* authService, QWidget *parent = nullptr);

private slots:
    void onLoginButtonClicked();

private:
    IAuthService* m_authService;
    QLineEdit *emailInput;
    QLineEdit *passwordInput;
    QCheckBox *rememberMeCheckbox;
    QPushButton *loginButton;
    QLabel *statusLabel;
};

#endif // LOGINPAGE_H
