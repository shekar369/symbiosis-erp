import { useState } from 'react';
import { Upload, CheckCircle2, AlertCircle, X } from '../../utils/icons';
import Button from './Button';
import api from '../../services/api';

const FileUpload = ({
  endpoint,
  acceptedFormats = '.xlsx,.xls',
  title = 'Upload File',
  onSuccess,
  onError
}) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setUploadResult(null);
      setShowResults(false);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await api.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadResult(response.data);
      setShowResults(true);
      setSelectedFile(null);

      if (onSuccess) {
        onSuccess(response.data);
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Upload failed';
      setUploadResult({
        success: false,
        message: errorMessage,
        errors: []
      });
      setShowResults(true);

      if (onError) {
        onError(error);
      }
    } finally {
      setUploading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setShowResults(false);
  };

  return (
    <div className="space-y-4">
      {/* File Selection */}
      <div className="flex items-center gap-3">
        <div className="flex-1">
          <label className="block">
            <input
              type="file"
              accept={acceptedFormats}
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
            />
            <div className="flex items-center gap-3 px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 cursor-pointer transition-colors">
              <Upload size={20} className="text-gray-400" />
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-700">
                  {selectedFile ? selectedFile.name : 'Choose a file or drag it here'}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Supported formats: {acceptedFormats}
                </p>
              </div>
            </div>
          </label>
        </div>

        {selectedFile && (
          <div className="flex gap-2">
            <Button
              onClick={handleUpload}
              disabled={uploading}
              icon={uploading ? null : <Upload size={16} />}
            >
              {uploading ? 'Uploading...' : 'Upload'}
            </Button>
            <Button
              variant="outline"
              onClick={handleClear}
              icon={<X size={16} />}
            >
              Clear
            </Button>
          </div>
        )}
      </div>

      {/* Upload Results */}
      {showResults && uploadResult && (
        <div className={`p-4 rounded-lg border-2 ${
          uploadResult.success
            ? 'bg-green-50 border-green-200'
            : 'bg-red-50 border-red-200'
        }`}>
          <div className="flex items-start gap-3">
            {uploadResult.success ? (
              <CheckCircle2 className="text-green-600 flex-shrink-0 mt-0.5" size={20} />
            ) : (
              <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
            )}
            <div className="flex-1">
              <p className={`font-medium ${
                uploadResult.success ? 'text-green-900' : 'text-red-900'
              }`}>
                {uploadResult.message}
              </p>

              {/* Summary */}
              {uploadResult.summary && (
                <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="text-sm">
                    <span className="text-gray-600">Total Rows:</span>
                    <span className="ml-2 font-semibold text-gray-900">
                      {uploadResult.summary.total_rows}
                    </span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-600">Uploaded:</span>
                    <span className="ml-2 font-semibold text-green-600">
                      {uploadResult.summary.uploaded}
                    </span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-600">Failed:</span>
                    <span className="ml-2 font-semibold text-red-600">
                      {uploadResult.summary.failed}
                    </span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-600">Validation Errors:</span>
                    <span className="ml-2 font-semibold text-orange-600">
                      {uploadResult.summary.validation_errors}
                    </span>
                  </div>
                </div>
              )}

              {/* Errors List */}
              {uploadResult.errors && uploadResult.errors.length > 0 && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">
                    Errors ({uploadResult.errors.length}):
                  </p>
                  <div className="max-h-48 overflow-y-auto space-y-1">
                    {uploadResult.errors.map((error, idx) => (
                      <div key={idx} className="text-xs bg-white p-2 rounded border border-gray-200">
                        <span className="font-medium">Row {error.row}:</span>
                        <span className="ml-2 text-gray-700">{error.column} - </span>
                        <span className="text-red-600">{error.error}</span>
                        {error.value && (
                          <span className="ml-2 text-gray-500">(Value: {error.value})</span>
                        )}
                      </div>
                    ))}
                  </div>
                  {uploadResult.errors.length >= 100 && (
                    <p className="text-xs text-gray-500 mt-2">
                      Showing first 100 errors only
                    </p>
                  )}
                </div>
              )}

              {/* Close Button */}
              <div className="mt-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowResults(false)}
                >
                  Close
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
