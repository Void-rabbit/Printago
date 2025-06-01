#include "mainwindow.h"
#include "loginpage.h" // Include the new LoginPage header
#include "dashboardpage.h" // Include the new DashboardPage header
#include "camerafeedpage.h" // Include the new CameraFeedPage header
#include "jobmanagementpage.h" // Include the new JobManagementPage header
#include "settingspage.h" // Include the new SettingsPage header
#include "services/MockAuthService.h" // Include the MockAuthService
#include "services/MockDataService.h" // Include the MockDataService
#include "services/MockCameraService.h" // Include the MockCameraService
#include <QLabel> // Still needed for placeholder pages
#include <QDebug> // For printing messages

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    // Set window title
    setWindowTitle("PrintagoQtApp");

    // Instantiate the auth service
    m_authService = new MockAuthService(this); // Parented to MainWindow for auto deletion
    // Instantiate the data service
    m_dataService = new MockDataService(this); // Parented to MainWindow for auto deletion
    // Instantiate the camera service
    m_cameraService = new MockCameraService(this); // Parented to MainWindow for auto deletion

    // Create a central widget and main layout
    QWidget *centralWidget = new QWidget(this);
    QHBoxLayout *mainLayout = new QHBoxLayout(centralWidget);

    // Create the navigation list
    navigationList = new QListWidget(this);
    navigationList->setMaximumWidth(150);
    navigationList->addItem("Login");
    navigationList->addItem("Dashboard");
    navigationList->addItem("Camera Feed");
    navigationList->addItem("Job Management");
    navigationList->addItem("Settings");

    // Create the stacked widget
    stackedWidget = new QStackedWidget(this);

    // Page 0: Login Page
    loginPage = new LoginPage(m_authService, this); // Pass auth service
    stackedWidget->addWidget(loginPage);

    // Page 1: Dashboard Page (placeholder first, then replace)
    QLabel* dashboardPlaceholder = new QLabel("Dashboard Page Placeholder (being replaced)", this);
    stackedWidget->addWidget(dashboardPlaceholder); // Added at index 1

    // Page 2: Camera Feed Page (placeholder first, then replace)
    QLabel* cameraFeedPlaceholder = new QLabel("Camera Feed Page Placeholder (being replaced)", this);
    stackedWidget->addWidget(cameraFeedPlaceholder); // Added at index 2

    // Page 3: Job Management Page (placeholder first, then replace)
    QLabel* jobManagementPlaceholder = new QLabel("Job Management Page Placeholder (being replaced)", this);
    stackedWidget->addWidget(jobManagementPlaceholder); // Added at index 3

    // Page 4: Settings Page (placeholder first, then replace)
    QLabel* settingsPlaceholder = new QLabel("Settings Page Placeholder (being replaced)", this);
    stackedWidget->addWidget(settingsPlaceholder); // Added at index 4

    // Now, replace the dashboard placeholder with the actual dashboard page
    dashboardPage = new DashboardPage(m_dataService, this); // Pass data service
    stackedWidget->removeWidget(dashboardPlaceholder); // Remove by pointer
    delete dashboardPlaceholder; // Delete the placeholder widget
    stackedWidget->insertWidget(1, dashboardPage); // Insert the actual page at index 1

    // Now, replace the camera feed placeholder with the actual camera feed page
    cameraFeedPage = new CameraFeedPage(m_cameraService, this); // Pass camera service
    stackedWidget->removeWidget(cameraFeedPlaceholder); // Remove by pointer
    delete cameraFeedPlaceholder; // Delete the placeholder widget
    stackedWidget->insertWidget(2, cameraFeedPage); // Insert the actual page at index 2

    // Now, replace the job management placeholder with the actual job management page
    jobManagementPage = new JobManagementPage(m_dataService, this); // Pass data service
    stackedWidget->removeWidget(jobManagementPlaceholder); // Remove by pointer
    delete jobManagementPlaceholder; // Delete the placeholder widget
    stackedWidget->insertWidget(3, jobManagementPage); // Insert the actual page at index 3

    // Now, replace the settings placeholder with the actual settings page
    settingsPage = new SettingsPage(m_dataService, this); // Pass data service
    stackedWidget->removeWidget(settingsPlaceholder); // Remove by pointer
    delete settingsPlaceholder; // Delete the placeholder widget
    stackedWidget->insertWidget(4, settingsPage); // Insert the actual page at index 4

    // Add widgets to the main layout
    mainLayout->addWidget(navigationList);
    mainLayout->addWidget(stackedWidget);

    // Set the central widget for the QMainWindow
    setCentralWidget(centralWidget);

    // Connect navigation list selection to stacked widget page changes
    connect(navigationList, &QListWidget::currentRowChanged, stackedWidget, &QStackedWidget::setCurrentIndex);

    // Attempt to load and apply the stylesheet
    QFile styleSheetFile("../static/css/dark_theme.qss"); // Path relative to build/execution dir
    if (styleSheetFile.open(QFile::ReadOnly | QFile::Text)) {
        QTextStream in(&styleSheetFile);
        QString styleSheet = in.readAll();
        styleSheetFile.close();
        qApp->setStyleSheet(styleSheet);
        qDebug() << "Stylesheet '../static/css/dark_theme.qss' loaded successfully.";
    } else {
        qDebug() << "Failed to load stylesheet '../static/css/dark_theme.qss'. Error: " << styleSheetFile.errorString();
    }
}

MainWindow::~MainWindow()
{
    // Destructor code, if needed
    // Qt handles child widget deletion automatically.
}
