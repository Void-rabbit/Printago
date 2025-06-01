#ifndef DASHBOARDPAGE_H
#define DASHBOARDPAGE_H

#include <QWidget>

// Forward declarations
class QLabel;
class QListWidget;
class QPushButton;
class QVBoxLayout;
class QHBoxLayout;
class IDataService; // Forward declaration

class DashboardPage : public QWidget
{
    Q_OBJECT

public:
    explicit DashboardPage(IDataService* dataService, QWidget *parent = nullptr);

private slots:
    void refreshPrinters();

private:
    IDataService* m_dataService;
    QLabel *titleLabel;
    QListWidget *printerListWidget;
    QPushButton *refreshButton;
};

#endif // DASHBOARDPAGE_H
