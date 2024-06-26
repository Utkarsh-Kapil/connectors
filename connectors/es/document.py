#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
from connectors.logger import DocumentLogger


class InvalidDocumentSourceError(Exception):
    pass


class ESDocument:
    """
    Represents a document in an Elasticsearch index.
    """

    def __init__(self, elastic_index, doc_source):
        self.index = elastic_index
        if not isinstance(doc_source, dict):
            msg = f"Invalid type found for doc_source: {type(doc_source).__name__}, expected: {dict.__name__}"
            raise InvalidDocumentSourceError(msg)
        self.id = doc_source.get("_id")
        if not isinstance(self.id, str):
            msg = f"Invalid type found for id: {type(self.id).__name__}, expected: {str.__name__}"
            raise InvalidDocumentSourceError(msg)
        self._seq_no = doc_source.get("_seq_no")
        self._primary_term = doc_source.get("_primary_term")
        self._source = doc_source.get("_source", {})
        if not isinstance(self._source, dict):
            msg = f"Invalid type found for source: {type(self._source).__name__}, expected: {dict.__name__}"
            raise InvalidDocumentSourceError(msg)
        self.logger = DocumentLogger(prefix=self._prefix(), extra=self._extra())

    def get(self, *keys, default=None):
        value = self._source
        for key in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(key)
        if value is None:
            return default
        return value

    async def reload(self):
        doc_source = await self.index.fetch_response_by_id(self.id)
        self._seq_no = doc_source.get("_seq_no")
        self._primary_term = doc_source.get("_primary_term")
        self._source = doc_source.get("_source", {})

    def log_debug(self, msg, *args, **kwargs):
        self.logger.debug(
            msg,
            *args,
            **kwargs,
        )

    def log_info(self, msg, *args, **kwargs):
        self.logger.info(
            msg,
            *args,
            **kwargs,
        )

    def log_warning(self, msg, *args, **kwargs):
        self.logger.warning(
            msg,
            *args,
            **kwargs,
        )

    def log_error(self, msg, *args, **kwargs):
        self.logger.error(
            msg,
            *args,
            **kwargs,
        )

    def log_exception(self, msg, *args, exc_info=True, **kwargs):
        self.logger.exception(
            msg,
            *args,
            exc_info=exc_info,
            **kwargs,
        )

    def log_critical(self, msg, *args, **kwargs):
        self.logger.critical(
            msg,
            *args,
            **kwargs,
        )

    def log_fatal(self, msg, *args, **kwargs):
        self.logger.fatal(
            msg,
            *args,
            **kwargs,
        )

    def _prefix(self):
        """Return a string which will be prefixed to the log message when filebeat is not turned on"""
        return None

    def _extra(self):
        """Return custom fields to be added to ecs logging when filebeat is turned on"""
        return {}
