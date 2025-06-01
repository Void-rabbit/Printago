#include "MockCameraService.h"
#include <QLabel>
#include <QTimer>
#include <QDebug>
#include <QVBoxLayout> // For centering text in the QLabel

MockCameraService::MockCameraService(QObject *parent) : QObject(parent)
{
}

MockCameraService::~MockCameraService()
{
    // Clean up the mock feed widgets
    qDeleteAll(m_mockFeedWidgets);
    m_mockFeedWidgets.clear();
}

QWidget* MockCameraService::getCameraFeedWidget(const QString& printerId)
{
    if (m_mockFeedWidgets.contains(printerId)) {
        return m_mockFeedWidgets[printerId];
    }

    QLabel* feedLabel = new QLabel("Camera Feed for " + printerId + "\n(Standby)");
    // feedLabel->setParent(nullptr); // Explicitly set no parent, service owns it.
                                 // CameraFeedPage will set parent when adding to its layout.
    feedLabel->setMinimumSize(320, 240); // A default size
    feedLabel->setAlignment(Qt::AlignCenter);
    feedLabel->setStyleSheet("background-color: black; color: lightgray; border: 1px solid gray;");
    QFont font = feedLabel->font();
    font.setPointSize(12);
    feedLabel->setFont(font);

    m_mockFeedWidgets.insert(printerId, feedLabel);
    return feedLabel;
}

void MockCameraService::startCameraFeed(
    const QString& printerId,
    std::function<void(bool success, const QString& message)> callback)
{
    qDebug() << "MockCameraService: Attempting to start feed for" << printerId;
    QLabel* feedWidget = m_mockFeedWidgets.value(printerId, nullptr);

    if (!feedWidget) {
        // Optionally create it here if getCameraFeedWidget wasn't called first
        // feedWidget = qobject_cast<QLabel*>(getCameraFeedWidget(printerId));
        // if (!feedWidget) {
            if (callback) {
                callback(false, "Feed widget not found for " + printerId + ". Call getCameraFeedWidget first.");
            }
            return;
        // }
    }

    // Final state of the widget will be set in the timer lambda
    feedWidget->setText("Starting feed for " + printerId + "...");

    QTimer::singleShot(200, this, [this, printerId, callback, feedWidget]() {
        if (feedWidget) { // Check again in case it was somehow deleted
            feedWidget->setText("Mock Camera Feed for " + printerId + "\n(LIVE)");
            feedWidget->setStyleSheet("background-color: darkgreen; color: white; border: 1px solid lime;"); // Indicate live
            qDebug() << "MockCameraService: Feed started for" << printerId;
        }
        if (callback) {
            callback(true, "Mock camera feed started for " + printerId);
        }
    });
}

void MockCameraService::stopCameraFeed(const QString& printerId)
{
    qDebug() << "MockCameraService: Stopping feed for" << printerId;
    if (m_mockFeedWidgets.contains(printerId)) {
        QLabel* feedWidget = m_mockFeedWidgets[printerId];
        feedWidget->setText("Mock Camera Feed for " + printerId + "\n(Stopped)");
        feedWidget->setStyleSheet("background-color: black; color: lightgray; border: 1px solid gray;"); // Back to standby look
    }
}
