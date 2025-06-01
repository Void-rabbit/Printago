#include "camerafeedpage.h"

#include <QLabel>
#include <QVBoxLayout>
#include <QHBoxLayout> // For controls
#include <QFrame>
#include <QFont> // For styling title
#include <QLineEdit> // Added
#include <QPushButton> // Added
#include <QDebug> // For messages

#include "Printago/Agents/ICameraService.h" // Full include

CameraFeedPage::CameraFeedPage(ICameraService* cameraService, QWidget *parent)
    : QWidget(parent), m_cameraService(cameraService), m_currentFeedWidget(nullptr)
{
    Q_ASSERT(m_cameraService != nullptr);
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setAlignment(Qt::AlignTop); // Align content to the top

    // Title
    titleLabel = new QLabel("Camera Feed", this);
    QFont titleFont = titleLabel->font();
    titleFont.setPointSize(16);
    titleFont.setBold(true);
    titleLabel->setFont(titleFont);
    titleLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(titleLabel, 0, Qt::AlignTop);
    mainLayout->addSpacing(10);

    // Controls Layout
    QHBoxLayout *controlsLayout = new QHBoxLayout();
    m_printerIdInput = new QLineEdit(this);
    m_printerIdInput->setPlaceholderText("Enter Printer ID (e.g., printer1)");
    controlsLayout->addWidget(m_printerIdInput);

    m_startFeedButton = new QPushButton("Start Feed", this);
    connect(m_startFeedButton, &QPushButton::clicked, this, &CameraFeedPage::onStartFeedClicked);
    controlsLayout->addWidget(m_startFeedButton);

    m_stopFeedButton = new QPushButton("Stop Feed", this);
    connect(m_stopFeedButton, &QPushButton::clicked, this, &CameraFeedPage::onStopFeedClicked);
    m_stopFeedButton->setEnabled(false); // Initially disabled
    controlsLayout->addWidget(m_stopFeedButton);
    mainLayout->addLayout(controlsLayout);
    mainLayout->addSpacing(5);

    // Status Label
    m_statusLabel = new QLabel("Enter a Printer ID and click 'Start Feed'.", this);
    m_statusLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(m_statusLabel);
    mainLayout->addSpacing(5);

    // Camera View Placeholder (Frame to host the feed widget)
    cameraViewPlaceholder = new QFrame(this);
    cameraViewPlaceholder->setMinimumSize(640, 480);
    cameraViewPlaceholder->setFrameStyle(QFrame::Panel | QFrame::Sunken);
    cameraViewPlaceholder->setLineWidth(1);
    cameraViewPlaceholder->setStyleSheet("background-color: #333;"); // Darker background for the frame
    // Ensure cameraViewPlaceholder has a layout to add the feed widget into
    QVBoxLayout *placeholderFrameLayout = new QVBoxLayout(cameraViewPlaceholder);
    placeholderFrameLayout->setContentsMargins(0,0,0,0); // No margins, feed widget should fill it
    cameraViewPlaceholder->setLayout(placeholderFrameLayout);
    mainLayout->addWidget(cameraViewPlaceholder, 1); // Allow placeholder to stretch

    setLayout(mainLayout);
}

void CameraFeedPage::onStartFeedClicked()
{
    QString printerId = m_printerIdInput->text().trimmed();
    if (printerId.isEmpty()) {
        m_statusLabel->setText("Please enter a Printer ID.");
        return;
    }

    if (m_currentFeedWidget) {
        // Remove and delete the old feed widget
        cameraViewPlaceholder->layout()->removeWidget(m_currentFeedWidget);
        delete m_currentFeedWidget; // Or m_currentFeedWidget->deleteLater();
        m_currentFeedWidget = nullptr;
    }

    m_currentFeedWidget = m_cameraService->getCameraFeedWidget(printerId);

    if (m_currentFeedWidget) {
        // Parent the feed widget to the placeholder frame if not already parented by service.
        // m_currentFeedWidget->setParent(cameraViewPlaceholder); // This might not be needed if service handles it.
        cameraViewPlaceholder->layout()->addWidget(m_currentFeedWidget);
        m_currentFeedWidget->show(); // Ensure it's visible

        m_statusLabel->setText(QString("Requesting feed for %1...").arg(printerId));
        m_startFeedButton->setEnabled(false);

        m_cameraService->startCameraFeed(printerId,
            [this, printerId](bool success, const QString& message) {
                m_startFeedButton->setEnabled(true);
                if (success) {
                    m_statusLabel->setText(QString("Feed started for %1: %2").arg(printerId).arg(message));
                    m_stopFeedButton->setEnabled(true);
                     qDebug() << "CameraFeedPage: Start feed success -" << message;
                } else {
                    m_statusLabel->setText(QString("Failed to start feed for %1: %2").arg(printerId).arg(message));
                    qWarning() << "CameraFeedPage: Start feed failed -" << message;
                    if (m_currentFeedWidget) {
                         // Optionally hide or show an error message on the widget itself
                        cameraViewPlaceholder->layout()->removeWidget(m_currentFeedWidget);
                        delete m_currentFeedWidget;
                        m_currentFeedWidget = nullptr;
                    }
                }
            });
    } else {
        m_statusLabel->setText(QString("Could not get camera feed widget for %1.").arg(printerId));
        qWarning() << "CameraFeedPage: getCameraFeedWidget returned null for" << printerId;
    }
}

void CameraFeedPage::onStopFeedClicked()
{
    QString printerId = m_printerIdInput->text().trimmed(); // Or store current active printerId
    if (printerId.isEmpty() && m_currentFeedWidget) {
         // Try to infer from m_currentFeedWidget if possible, or disable stop if no ID.
         // For this mock, assume printerIdInput is still relevant or we stored it.
         // This part needs robust handling in a real app.
        qWarning("CameraFeedPage: No printer ID to stop feed. User might have cleared input.");
        // m_statusLabel->setText("No printer ID specified to stop feed.");
        // return;
        // For now, let's assume m_printerIdInput still holds the ID of the active feed
    }


    if (m_currentFeedWidget) { // Check if there's an active feed widget
         m_statusLabel->setText(QString("Stopping feed for %1...").arg(printerId));
         m_cameraService->stopCameraFeed(printerId);
         m_stopFeedButton->setEnabled(false);
         m_startFeedButton->setEnabled(true); // Allow trying to start again
         // The MockService will change the widget's text.
         // We don't delete m_currentFeedWidget here as the service might reuse it or manage its text.
         // If CameraFeedPage should fully remove it:
         // cameraViewPlaceholder->layout()->removeWidget(m_currentFeedWidget);
         // delete m_currentFeedWidget; // if this page owns it after getting it
         // m_currentFeedWidget = nullptr;
         m_statusLabel->setText(QString("Feed stopped for %1.").arg(printerId));
         qDebug() << "CameraFeedPage: Feed stopped for" << printerId;
    } else {
        m_statusLabel->setText("No active feed to stop.");
        qDebug() << "CameraFeedPage: Stop feed clicked but no m_currentFeedWidget.";
        m_stopFeedButton->setEnabled(false);
    }
}
