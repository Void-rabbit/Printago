#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QStackedWidget>
#include <QListWidget>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QWidget>
#include <QFile>
#include <QTextStream>
#include <QApplication>

class QLabel; // Forward declaration still needed if statusLabel is kept or for placeholder pages
class LoginPage; // Forward declaration for LoginPage
class DashboardPage; // Forward declaration for DashboardPage
class CameraFeedPage; // Forward declaration for CameraFeedPage
class JobManagementPage; // Forward declaration for JobManagementPage
class SettingsPage; // Forward declaration for SettingsPage
class IAuthService; // Forward declaration for the service interface
class IDataService; // Forward declaration for the data service interface
class ICameraService; // Forward declaration for the camera service interface

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    QLabel *statusLabel; // Example member
    QStackedWidget *stackedWidget;
    QListWidget *navigationList;
    LoginPage *loginPage;
    DashboardPage *dashboardPage;
    CameraFeedPage *cameraFeedPage;
    JobManagementPage *jobManagementPage;
    SettingsPage *settingsPage;
    IAuthService* m_authService;
    IDataService* m_dataService;
    ICameraService* m_cameraService;
};

#endif // MAINWINDOW_H
