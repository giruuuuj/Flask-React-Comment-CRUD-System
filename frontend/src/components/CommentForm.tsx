import React, { useState } from 'react';

interface CommentFormProps {
  onSubmit: (data: { content: string; author_name: string; author_email?: string }) => void;
  submitText: string;
  initialValues: { content: string; author_name: string; author_email?: string };
  onCancel?: () => void;
}

const CommentForm: React.FC<CommentFormProps> = ({
  onSubmit,
  submitText,
  initialValues,
  onCancel,
}) => {
  const [formData, setFormData] = useState(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    const newErrors: Record<string, string> = {};
    if (!formData.content.trim()) {
      newErrors.content = 'Content is required';
    }
    if (!formData.author_name.trim()) {
      newErrors.author_name = 'Author name is required';
    }
    if (formData.author_email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.author_email)) {
      newErrors.author_email = 'Invalid email format';
    }
    
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length === 0) {
      onSubmit(formData);
      if (!onCancel) {
        setFormData({ content: '', author_name: '', author_email: '' });
      }
    }
    
    setIsSubmitting(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="comment-form">
      <div className="form-group">
        <label htmlFor="author_name">Name *</label>
        <input
          type="text"
          id="author_name"
          name="author_name"
          value={formData.author_name}
          onChange={handleChange}
          className={errors.author_name ? 'error' : ''}
          placeholder="Your name"
        />
        {errors.author_name && <span className="error-text">{errors.author_name}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="author_email">Email (optional)</label>
        <input
          type="email"
          id="author_email"
          name="author_email"
          value={formData.author_email || ''}
          onChange={handleChange}
          className={errors.author_email ? 'error' : ''}
          placeholder="your@email.com"
        />
        {errors.author_email && <span className="error-text">{errors.author_email}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="content">Comment *</label>
        <textarea
          id="content"
          name="content"
          value={formData.content}
          onChange={handleChange}
          className={errors.content ? 'error' : ''}
          placeholder="Write your comment here..."
          rows={4}
        />
        {errors.content && <span className="error-text">{errors.content}</span>}
      </div>

      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting ? 'Submitting...' : submitText}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="btn btn-secondary">
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default CommentForm;
