# -*- coding: utf-8 -*-

from app import app, db

class VulnCve(db.Model):
    """
    Store CVE
    """
    __tablename__='vulncve'
    friendly_name = "Vulnerability CVE"

    id = db.Column(db.Integer(), primary_key=True)
    cve_id = db.Column(db.String(20))
    version = db.Column(db.String())
    description = db.Column(db.String())
    url = db.Column(db.String())
    status = db.Column(db.String())

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during save operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during delete operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def __repr__(self):
        return self.name

class VulnBasic(db.Model):

    """
    Basic Vulnerability
    """
    __tablename__='vulnbasic'
    friendly_name = "Vulnerability Basic"
        
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String())
    match = db.Column(db.String())
    expectmatch = db.Column(db.Integer())

#    configurationvalues_id = db.Column(db.Integer(), db.ForeignKey('configurationvalues.id'))
#    configurationvalues = db.relationship('confvalues_vulnbasic', backref='vulnbasic', lazy='dynamic')

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during save operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during delete operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def __repr__(self):
        return self.name

class ConfVuln(db.Model):
    """
    Represents a Vulnerability in a conf
    """
    __tablename__='confvuln'
    friendly_name = "Configuration Vulnerability"

    id = db.Column(db.Integer, primary_key=True)
    configuration_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))
    vulnbasic_id = db.Column(db.Integer, db.ForeignKey('vulnbasic.id'))
    vulncve_id = db.Column(db.Integer, db.ForeignKey('vulncve.id'))
    date = db.Column(db.DateTime())

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during save operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during delete operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def __repr__(self):
        return self.path


class VulnPerm(db.Model):

    """
    Permisssive Vulnerability
    """
    __tablename__='vulnperm'
    friendly_name = "Vulnerability Permissive"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    match = db.Column(db.String())

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during save operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during delete operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def __repr__(self):
        return self.name
