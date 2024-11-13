import React from 'react';

function ProjectDetails({ project }) {
    return (
        <div className="project-details">
            <div className="project-header">
                <h2>{project.projectName}</h2>
                <div className="project-info">
                    <p><strong>Project ID:</strong> {project.projectId}</p>
                    <p><strong>Description:</strong> {project.description || 'No description provided'}</p>
                </div>
            </div>
            
            <div className="project-members">
                <h3>Project Members</h3>
                <div className="member-list">
                    {project.members?.map(member => (
                        <div key={member} className={`member-item ${member === project.creator ? 'creator' : ''}`}>
                            {member} {member === project.creator && '(Creator)'}
                        </div>
                    ))}
                </div>
            </div>

            <div className="project-hardware">
                <h3>Hardware Allocation</h3>
                {Object.entries(project.hardware || {}).map(([hwName, quantity]) => (
                    <div key={hwName} className="hardware-allocation">
                        <span>{hwName}:</span>
                        <span>{quantity} units checked out</span>
                    </div>
                ))}
                <div className="hardware-status">
                    <p className="hardware-note">
                        {Object.values(project.hardware || {}).some(qty => qty > 0)
                            ? "Use the hardware section below to check in equipment"
                            : "No hardware currently checked out"}
                    </p>
                </div>
            </div>
        </div>
    );
}

export default ProjectDetails;