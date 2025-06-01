#ifndef JOBMANAGEMENTPAGE_H
#define JOBMANAGEMENTPAGE_H

#include <QWidget>

// Forward declarations
class QLabel;
class QListWidget;
class QPushButton;
class QVBoxLayout;
class QHBoxLayout;
class IDataService; // Forward declaration

class JobManagementPage : public QWidget
{
    Q_OBJECT

public:
    explicit JobManagementPage(IDataService* dataService, QWidget *parent = nullptr);

private slots:
    void refreshJobs();
    void updateButtonStates(); // Slot to manage button enable/disable

private:
    IDataService* m_dataService;
    QLabel *titleLabel;
    QListWidget *jobListWidget;
    QPushButton *refreshJobsButton; // Added for consistency
    QPushButton *startJobButton;
    QPushButton *pauseJobButton;
    QPushButton *cancelJobButton;
};

#endif // JOBMANAGEMENTPAGE_H
