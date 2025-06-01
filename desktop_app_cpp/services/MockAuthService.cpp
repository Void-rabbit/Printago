#include "MockAuthService.h"
#include <QTimer>
#include <QDebug> // For logging, optional

MockAuthService::MockAuthService(QObject *parent) : QObject(parent)
{
    // Constructor, if anything needed
}

void MockAuthService::login(
    const QString& email,
    const QString& password,
    std::function<void(bool success, const QString& message)> callback)
{
    qDebug() << "MockAuthService: Attempting login for email" << email;

    // Simulate a network delay
    QTimer::singleShot(1000, this, [this, email, password, callback]() {
        if (email == "test@example.com" && password == "password") {
            m_isLoggedIn = true;
            m_currentUserEmail = email;
            qDebug() << "MockAuthService: Login successful for" << email;
            if (callback) {
                callback(true, "Login successful!");
            }
        } else {
            m_isLoggedIn = false;
            m_currentUserEmail.clear();
            qDebug() << "MockAuthService: Login failed for" << email;
            if (callback) {
                callback(false, "Invalid credentials. (Mock response)");
            }
        }
    });
}

void MockAuthService::logout()
{
    qDebug() << "MockAuthService: Logging out" << m_currentUserEmail;
    m_isLoggedIn = false;
    m_currentUserEmail.clear();
    // In a real scenario, might need to notify other parts of the app
}

bool MockAuthService::isLoggedIn() const
{
    return m_isLoggedIn;
}

QString MockAuthService::getCurrentUserEmail() const
{
    return m_currentUserEmail;
}
