#ifndef CAMERAFEEDPAGE_H
#define CAMERAFEEDPAGE_H

#include <QWidget>

// Forward declarations
class QLabel;
class QVBoxLayout;
class QFrame;
class QLineEdit; // Added
class QPushButton; // Added
class ICameraService; // Forward declaration

class CameraFeedPage : public QWidget
{
    Q_OBJECT

public:
    explicit CameraFeedPage(ICameraService* cameraService, QWidget *parent = nullptr);

private slots:
    void onStartFeedClicked();
    void onStopFeedClicked();

private:
    ICameraService* m_cameraService;
    QLabel *titleLabel;
    QFrame *cameraViewPlaceholder; // This frame will host the feed widget
    QWidget* m_currentFeedWidget;  // The actual feed widget from the service
    QLineEdit* m_printerIdInput;
    QPushButton* m_startFeedButton;
    QPushButton* m_stopFeedButton;
    QLabel* m_statusLabel; // For messages from the service
};

#endif // CAMERAFEEDPAGE_H
