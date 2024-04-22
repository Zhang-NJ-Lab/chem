import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
import pandas as pd
from chemdataextractor import Document


class ChemExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.file_label = QLabel("Input CSV File Path:")
        self.file_edit = QLineEdit()
        self.file_button = QPushButton("Browse")
        self.file_button.clicked.connect(self.browse_file)

        self.column_label = QLabel("Name of First Column:")
        self.column_edit = QLineEdit()

        self.output_label = QLabel("Output CSV File Path:")
        self.output_edit = QLineEdit()
        self.output_button = QPushButton("Browse")
        self.output_button.clicked.connect(self.browse_output)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_extraction)

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_edit)
        layout.addWidget(self.file_button)
        layout.addWidget(self.column_label)
        layout.addWidget(self.column_edit)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_edit)
        layout.addWidget(self.output_button)
        layout.addWidget(self.run_button)

        self.setLayout(layout)
        self.setWindowTitle("Chemical Extractor")
        self.show()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.file_edit.setText(file_path)

    def browse_output(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if output_path:
            self.output_edit.setText(output_path)

    def is_chemical(self, entity):
        doc = Document(entity)
        chem_entities = doc.cems
        return len(chem_entities) > 0

    def run_extraction(self):
        input_file = self.file_edit.text()
        column_name = self.column_edit.text()
        output_file = self.output_edit.text()

        try:
            df = pd.read_csv(input_file, encoding='gb18030')
            column_data = df[column_name]
            df['Chemical'] = column_data.apply(lambda x: 1 if self.is_chemical(x) else 0)
            df = df[df.iloc[:, -1] != 0]
            df = df.drop(df.columns[-1], axis=1)
            df.to_csv(output_file, index=False)
            QMessageBox.information(self, "Extraction Complete", "Chemical extraction completed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChemExtractorApp()
    sys.exit(app.exec_())
