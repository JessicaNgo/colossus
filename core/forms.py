"""
Created on May 24, 2016

@author: Jafar Taghiyar (jtaghiyar@bccrc.ca)

Updated Nov 3, 2017 by Spencer Vatrt-Watts (github.com/Spenca)
"""

import os

#===========================
# Django imports
#---------------------------
from django.forms import (
    ModelForm,
    Form,
    CharField,
    FileField,
    EmailField,
    DateField,
    BooleanField,
    ChoiceField,
    ValidationError,
    inlineformset_factory,
    BaseInlineFormSet
)
from django.forms.extras.widgets import SelectDateWidget


#===========================
# App imports
#---------------------------
from .models import (
    Sample,
    AdditionalSampleInformation,
    Library,
    PbalLibrary,
    TenxLibrary,
    SublibraryInformation,
    LibrarySampleDetail,
    LibraryConstructionInformation,
    LibraryQuantificationAndStorage,
    PbalLibrarySampleDetail,
    PbalLibraryConstructionInformation,
    PbalLibraryQuantificationAndStorage,
    TenxLibrarySampleDetail,
    TenxLibraryConstructionInformation,
    TenxLibraryQuantificationAndStorage,
    Sequencing,
    SequencingDetail,
    PbalSequencing,
    PbalSequencingDetail,
    TenxSequencing,
    TenxSequencingDetail,
    Lane,
    PbalLane,
    TenxLane,
    Plate
)
from .utils import parse_smartchipapp_results_file


#===========================
# 3rd-party app imports
#---------------------------
from taggit.models import Tag


#===========================
# Helpers
#---------------------------
class SaveDefault(ModelForm):

    """
    Save the default values all the time.
    """

    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will
        get validated and saved."""
        return True


#===========================
# Sample forms
#---------------------------
class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = "__all__"
        widgets = {
            'xenograft_biopsy_date': SelectDateWidget(
                years=range(2000, 2020),
                empty_label=('year', 'month', 'day'),
            )
        }
        labels = {
            'sample_id': ('*Sample ID'),
        }
        help_texts = {
            'sample_id': ('Sequencing ID (usually SA ID).'),
            'anonymous_patient_id': ('Original/clinical patient ID.'),
        }

    def clean(self):
        # if it's a new instance, the sample_id should not exist.
        if not self.instance.pk:
            cleaned_data = super(SampleForm, self).clean()
            sample_id = cleaned_data.get("sample_id")
            if len(Sample.objects.filter(sample_id=sample_id)):
                msg = "Sample ID already exists."
                self.add_error('sample_id', msg)

AdditionalSampleInfoInlineFormset =  inlineformset_factory(
    Sample,
    AdditionalSampleInformation,
    form = SaveDefault,
    fields = "__all__",
    widgets = {
        'patient_biopsy_date': SelectDateWidget(
            years=range(2000, 2020),
            empty_label=('year', 'month', 'day'),
        )
    },
    labels = {
        'tissue_type':('*Tissue type'),
        'anatomic_site':('*Anatomic site'),
    },
)


#===========================
# Library forms
#---------------------------
class LibraryForm(ModelForm):
    class Meta:
        model = Library
        exclude = ['num_sublibraries']
        labels = {
            'primary sample': ('*Sample'),
            'pool_id': ('*Chip ID'),
            'jira_ticket': ('*Jira Ticket'),
        }
        help_texts = {
            'sample': ('Sequencing ID (usually SA ID) of the sample composing the majority of the library.'),
            'pool_id': ('Chip ID.'),
            'jira_ticket': ('Jira Ticket.'),
        }

    def clean(self):
        # if it's a new instance, the pool_id should not exist.
        if not self.instance.pk:
            cleaned_data = super(LibraryForm, self).clean()
            pool_id = cleaned_data.get("pool_id")
            if len(Library.objects.filter(pool_id=pool_id)):
                msg = "Chip ID already exists."
                self.add_error('pool_id', msg)

class PbalLibraryForm(ModelForm):
    class Meta:
        model = PbalLibrary
        exclude = []
        labels = {
            'primary sample': ('*Sample'),
            'jira_ticket': ('*Jira Ticket'),
        }
        help_texts = {
            'sample': ('Sequencing ID (usually SA ID) of the sample composing the majority of the library.'),
            'jira_ticket': ('Jira Ticket.'),
        }

class TenxLibraryForm(ModelForm):
    class Meta:
        model = TenxLibrary
        exclude = []
        labels = {
            'primary sample': ('*Sample'),
            'jira_ticket': ('*Jira Ticket'),
        }
        help_texts = {
            'sample': ('Sequencing ID (usually SA ID) of the sample composing the majority of the library.'),
            'jira_ticket': ('Jira Ticket.'),
        }

class SublibraryForm(Form):
    # SmartChipApp results file
    smartchipapp_results_file = FileField(
        label="SmartChipApp results:",
        required=False,
    )

    def clean_smartchipapp_results_file(self):
        filename = self.cleaned_data['smartchipapp_results_file']
        if filename:
            try:
                results, region_metadata = parse_smartchipapp_results_file(filename)
                self.cleaned_data['smartchipapp_results'] = results
                self.cleaned_data['smartchipapp_region_metadata'] = region_metadata
            except ValueError as e:
                self.add_error('smartchipapp_results_file', ' '.join(e.args))
            except Exception as e:
                self.add_error('smartchipapp_results_file', 'failed to parse the file.')

class LibraryQuantificationAndStorageForm(ModelForm):

    """
    Clean uploaded files.
    """

    class Meta:
        model = LibraryQuantificationAndStorage
        fields = "__all__"

    def clean(self):
        """if Freezer specified, so should Rack,Shelf,Box,Positoin in box."""
        cleaned_data = super(LibraryQuantificationAndStorageForm, self).clean()
        freezer = cleaned_data.get('freezer')
        if freezer != '':
            if cleaned_data.get('rack') is None:
                msg = "Rack is required when specifying the Freezer."
                self.add_error('rack', msg)

            if cleaned_data.get('shelf') is None:
                msg = "Shelf is required when specifying the Freezer."
                self.add_error('shelf', msg)

            if cleaned_data.get('box') is None:
                msg = "Box is required when specifying the Freezer."
                self.add_error('box', msg)

            if cleaned_data.get('position_in_box') is None:
                msg = "Position in box is required when specifying the Freezer."
                self.add_error('position_in_box', msg)
        return cleaned_data

    def clean_agilent_bioanalyzer_xad(self):
        """check if it's a right filetype."""
        file = self.cleaned_data['agilent_bioanalyzer_xad']
        if file:
            _, ext = os.path.splitext(file.name)
            if ext != '.xad':
                msg = "file not supported with extension: %s" % ext
                self.add_error('agilent_bioanalyzer_xad', msg)
        return file

    def clean_agilent_bioanalyzer_image(self):
        """check if it's a right filetype."""
        file = self.cleaned_data['agilent_bioanalyzer_image']
        if file:
            _, ext = os.path.splitext(file.name)
            if ext.lower() not in ('.png', '.jpg', '.jpeg', '.bmp'):
                msg = "file not supported with extension: %s" % ext
                self.add_error('agilent_bioanalyzer_image', msg)
        return file

    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will
        get validated and saved."""
        return True

LibrarySampleDetailInlineFormset = inlineformset_factory(
    Library,
    LibrarySampleDetail,
    form = SaveDefault,
    fields = "__all__",
    widgets = {
        'sample_spot_date': SelectDateWidget(
            years=range(2000,2020),
            empty_label=('year', 'month', 'day'),
        )
    }
)

LibraryConstructionInfoInlineFormset =  inlineformset_factory(
    Library,
    LibraryConstructionInformation,
    form = SaveDefault,
    fields = "__all__",
    widgets = {
        'library_prep_date': SelectDateWidget(
            years=range(2000,2020),
            empty_label=('year', 'month', 'day'),
        )
    }
)

LibraryQuantificationAndStorageInlineFormset =  inlineformset_factory(
    Library,
    LibraryQuantificationAndStorage,
    form = LibraryQuantificationAndStorageForm,
    fields = "__all__",
    help_texts = {
        'agilent_bioanalyzer_xad': ('Select a xad file to upload.'),
        'agilent_bioanalyzer_png': ('Supported formats: png, jpg, jpeg, bmp.'),
    }
)

class PbalLibraryQuantificationAndStorageForm(ModelForm):

    """
    Clean uploaded files.
    """

    class Meta:
        model = PbalLibraryQuantificationAndStorage
        fields = "__all__"

    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will
        get validated and saved."""
        return True

PbalLibrarySampleDetailInlineFormset = inlineformset_factory(
    PbalLibrary,
    PbalLibrarySampleDetail,
    form = SaveDefault,
    fields = "__all__",
    widgets = {
        'sample_spot_date': SelectDateWidget(
            years=range(2000,2020),
            empty_label=('year', 'month', 'day'),
        )
    }    
)

PbalLibraryConstructionInfoInlineFormset =  inlineformset_factory(
    PbalLibrary,
    PbalLibraryConstructionInformation,
    form = SaveDefault,
    fields = "__all__",
    widgets = {
        'library_prep_date': SelectDateWidget(
            years=range(2000,2020),
            empty_label=('year', 'month', 'day'),
        )
    }
)

PbalLibraryQuantificationAndStorageInlineFormset =  inlineformset_factory(
    PbalLibrary,
    PbalLibraryQuantificationAndStorage,
    form = PbalLibraryQuantificationAndStorageForm,
    fields = "__all__",
)

class TenxLibraryQuantificationAndStorageForm(ModelForm):

    """
    Clean uploaded files.
    """

    class Meta:
        model = TenxLibraryQuantificationAndStorage
        fields = "__all__"

    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will
        get validated and saved."""
        return True

TenxLibrarySampleDetailInlineFormset = inlineformset_factory(
    TenxLibrary,
    TenxLibrarySampleDetail,
    form = SaveDefault,
    fields = "__all__",
    widgets = {
        'sample_prep_date': SelectDateWidget(
            years=range(2000,2020),
            empty_label=('year', 'month', 'day'),
        )
    }
)

TenxLibraryConstructionInfoInlineFormset =  inlineformset_factory(
    TenxLibrary,
    TenxLibraryConstructionInformation,
    form = SaveDefault,
    fields = "__all__",
    widgets = {
        'library_prep_date': SelectDateWidget(
            years=range(2000,2020),
            empty_label=('year', 'month', 'day'),
        )
    }
)

TenxLibraryQuantificationAndStorageInlineFormset =  inlineformset_factory(
    TenxLibrary,
    TenxLibraryQuantificationAndStorage,
    form = TenxLibraryQuantificationAndStorageForm,
    fields = "__all__",
)


#===========================
# Project forms
#---------------------------
class ProjectForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


#===========================
# Sequencing forms
#---------------------------
class SequencingForm(ModelForm):
    class Meta:
        model = Sequencing
        exclude = ['pool_id']
        widgets = {
            'submission_date': SelectDateWidget(
                years=range(2000,2020),
                empty_label=('year', 'month', 'day'),
            )
        }
        labels = {
            'library': ('*Library'),
        }
        help_texts = {
            'library': ('Select a library.'),
        }

SequencingDetailInlineFormset = inlineformset_factory(
    Sequencing,
    SequencingDetail,
    form = SaveDefault,
    fields = "__all__",
)

class PbalSequencingForm(ModelForm):
    class Meta:
        model = PbalSequencing
        exclude = ['pool_id']
        widgets = {
            'submission_date': SelectDateWidget(
                years=range(2000,2020),
                empty_label=('year', 'month', 'day'),
            )
        }
        labels = {
            'library': ('*Library'),
        }
        help_texts = {
            'library': ('Select a library.'),
        }

PbalSequencingDetailInlineFormset = inlineformset_factory(
    PbalSequencing,
    PbalSequencingDetail,
    form = SaveDefault,
    fields = "__all__",
)

class TenxSequencingForm(ModelForm):
    class Meta:
        model = TenxSequencing
        exclude = ['pool_id']
        widgets = {
            'submission_date': SelectDateWidget(
                years=range(2000,2020),
                empty_label=('year', 'month', 'day'),
            )
        }
        labels = {
            'library': ('*Library'),
        }
        help_texts = {
            'library': ('Select a library.'),
        }

TenxSequencingDetailInlineFormset = inlineformset_factory(
    TenxSequencing,
    TenxSequencingDetail,
    form = SaveDefault,
    fields = "__all__",
)


#===========================
# Lane forms
#---------------------------
class LaneForm(ModelForm):
    class Meta:
        model = Lane
        fields = "__all__"

class PbalLaneForm(ModelForm):
    class Meta:
        model = PbalLane
        fields = "__all__"

class TenxLaneForm(ModelForm):
    class Meta:
        model = TenxLane
        fields = "__all__"


#===========================
# Plate form
#---------------------------
class PlateForm(ModelForm):
    class Meta:
        model = Plate
        fields = "__all__"


#===========================
# GSC submission forms
#---------------------------
class GSCFormDeliveryInfo(Form):

    """
    Delivery information section of GSC submission form.
    """

    # fields
    name = CharField(
        label="Name",
        max_length=100,
        initial="Andy Mungall, Room 508",
    )
    org = CharField(
        label="Organization",
        max_length=100,
        initial="Biospecimen Core, Genome Sciences Centre, BC Cancer Agency",
    )
    addr = CharField(
        label="Address",
        max_length=100,
        initial="Suite 100, 570 West 7th Avenue, Vancouver, BC  V5Z 4S6, Canada",
    )
    email = EmailField(
        label="Email",
        initial="amungall@bcgsc.ca",
    )
    tel = CharField(
        label="Tel",
        max_length=100,
        initial="604-707-5900 ext 673251",
    )

class GSCFormSubmitterInfo(Form):

    """
    Delivery information section of GSC submission form.
    """

    # choices
    at_completion_choices = (
        ('R', 'Return unused sample'),
        ('D', 'Destroy unused sample'),
    )

    # fields
    submitter_name = CharField(
        label="Name of Submitter",
        max_length=100,
    )
    submitter_email = EmailField(
        label="Submitter's email",
    )
    submission_date = DateField(
        label="Submission Date",
        help_text = 'yyyy-mm-dd',
    )
    submitting_org = CharField(
        label="Submitting Organization",
        max_length=100,
        initial="BCCRC/ UBC",
    )
    pi_name = CharField(
        label="Name of Principal Investigator",
        max_length=100,
        initial="Sam Aparicio/ Carl Hansen",
    )
    pi_email = EmailField(
        label="Principal Investigator's email",
        initial="saparicio@bccrc.ca",
    )
    project_name = CharField(
        label="Project Name",
        max_length=100,
        initial="Single cell indexing",
    )
    sow = CharField(
        label="Statement of Work (SOW) #",
        max_length=100,
        initial="GSC-0297",
    )
    nextera_compatible = BooleanField(
        label="Nextera compatible",
        required=False,
        initial=True,
    )
    truseq_compatible = BooleanField(
        label="TruSeq compatible",
        required=False,
    )
    bsgsc_standard = BooleanField(
        label='BC GSC Standard',
        required=False,
    )
    custom = BooleanField(
        label="Custom",
        required=False,
    )
    is_this_pbal_library = BooleanField(
        label="Is this pbal library",
        required=False,
    )
    is_this_chromium_library = BooleanField(
        label="Is this Chromium library",
        required=False,
    )
    at_completion = ChoiceField(
        label="At completion of project",
        choices=at_completion_choices,
        initial='R',
    )